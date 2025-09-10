import { useEffect, useState, useMemo } from "react";
import Dropzone from "../components/Dropzone";

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { FileText, Trash2, CheckCircle, AlertCircle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { useUploadXml } from "@/hooks/useUploadXml";

export default function Home() {
  const [files, setFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState(null); // 'success', 'error', null
  const [uploadResult, setUploadResult] = useState(null);
  const uploadMutation = useUploadXml();

  // impedir que o browser tente abrir o arquivo ao soltar fora da dropzone
  useEffect(() => {
    const prevent = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };
    window.addEventListener("dragover", prevent);
    window.addEventListener("drop", prevent);
    return () => {
      window.removeEventListener("dragover", prevent);
      window.removeEventListener("drop", prevent);
    };
  }, []);

  // receber novos arquivos do Dropzone (append, evitando duplicados por nome+tamanho)
  function handleAddFiles(newList) {
    setFiles((prev) => {
      const map = new Map(prev.map((f) => [f.name + "::" + f.size, f]));
      newList.forEach((f) => map.set(f.name + "::" + f.size, f));
      return Array.from(map.values());
    });
  }

  function handleRemoveAt(idx) {
    setFiles((prev) => prev.filter((_, i) => i !== idx));
  }

  function handleClear() {
    setFiles([]);
  }

  const hasFiles = files.length > 0;
  const isUploading = uploadMutation.isPending;

  const totalSize = useMemo(
    () => files.reduce((acc, f) => acc + (f?.size || 0), 0),
    [files]
  );

  // Componente de Status de Upload
  function UploadStatus() {
    if (!uploadStatus) return null;

    if (uploadStatus === 'success') {
      return (
        <div className="flex items-center gap-3 p-4 rounded-xl bg-green-50 border border-green-200 text-green-800">
          <CheckCircle className="h-5 w-5 text-green-600" />
          <div className="flex-1">
            <p className="font-medium">Upload realizado com sucesso!</p>
            <p className="text-sm text-green-600">
              {uploadResult?.qtd_arquivos_processados} arquivo(s) processado(s) e {uploadResult?.data?.length || 0} registro(s) inserido(s) no banco.
            </p>
          </div>
        </div>
      );
    }

    if (uploadStatus === 'error') {
      return (
        <div className="flex items-center gap-3 p-4 rounded-xl bg-red-50 border border-red-200 text-red-800">
          <AlertCircle className="h-5 w-5 text-red-600" />
          <div className="flex-1">
            <p className="font-medium">Erro no upload</p>
            <p className="text-sm text-red-600">
              Verifique o arquivo e tente novamente.
            </p>
          </div>
        </div>
      );
    }

    return null;
  }

  function fmtBytes(n) {
    if (!n) return "0 B";
    const k = 1024;
    const units = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(n) / Math.log(k));
    return `${(n / Math.pow(k, i)).toFixed(i ? 1 : 0)} ${units[i]}`;
  }

  function handleProcess() {
    if (!hasFiles || uploadMutation.isPending) return;
    
    setUploadStatus(null);
    setUploadResult(null);
    
    uploadMutation.mutate(files, {
      onSuccess: (data) => {
        setUploadStatus('success');
        setUploadResult(data);
        toast.success(`Arquivos processados com sucesso! ${data.qtd_arquivos_processados} arquivo(s) processado(s).`);
        handleClear();
        
        // Limpar status de sucesso após 5 segundos
        setTimeout(() => {
          setUploadStatus(null);
          setUploadResult(null);
        }, 5000);
      },
      onError: (err) => {
        setUploadStatus('error');
        const msg =
          err?.response?.data?.detail ||
          err?.response?.data?.message ||
          err?.message ||
          "Erro ao enviar arquivos. Tente novamente.";
        toast.error(msg);
        
        // Limpar status de erro após 5 segundos
        setTimeout(() => {
          setUploadStatus(null);
          setUploadResult(null);
        }, 5000);
      },
    });
  }

  // ====== RENDER ======
  if (!hasFiles) {
    // estado vazio — tela centralizada
    return (
      <section className="grid place-items-center min-h-[calc(100dvh-56px)] p-4">
        <Card className="w-full max-w-3xl rounded-2xl border border-border bg-card shadow-sm">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-semibold">Importar XML</CardTitle>
            <CardDescription>
              Arraste o arquivo .xml ou clique para selecionar
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            <Dropzone onFiles={handleAddFiles} disabled={isUploading} />

            <UploadStatus />

            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Button
                onClick={handleProcess}
                disabled={!hasFiles || isUploading}
                className="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processando...
                  </>
                ) : (
                  "Enviar XML"
                )}
              </Button>
              <Button
                variant="outline"
                onClick={handleClear}
                disabled={isUploading}
                className="w-full sm:w-auto border-green-200 text-green-700 hover:bg-green-50"
              >
                Limpar
              </Button>
            </div>
          </CardContent>
        </Card>
      </section>
    );
  }

  // estado com arquivos — layout split
  return (
    <section
      className={cn(
        "mx-auto w-full p-4",
        "grid gap-6",
        // em telas grandes vira duas colunas: conteúdo | painel de arquivos
        "lg:grid-cols-[minmax(0,1fr)_420px]"
      )}
    >
      {/* Coluna esquerda: card com dropzone + ações */}
      <Card className="rounded-2xl border border-border bg-card shadow-sm">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-semibold">Importar XML</CardTitle>
          <CardDescription>
            Arraste os arquivos .xml ou clique para selecionar
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-6">
          <Dropzone onFiles={handleAddFiles} disabled={isUploading} />

          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>{files.length} arquivo(s)</span>
            <span>{fmtBytes(totalSize)}</span>
          </div>

          <UploadStatus />

          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Button
              onClick={handleProcess}
              disabled={!hasFiles || isUploading}
              className="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white"
            >
              {isUploading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Processando...
                </>
              ) : (
                "Enviar XML"
              )}
            </Button>
            <Button
              variant="outline"
              onClick={handleClear}
              disabled={isUploading}
              className="w-full sm:w-auto border-green-200 text-green-700 hover:bg-green-50"
            >
              Limpar
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Coluna direita: painel com lista de arquivos */}
      <Card className="rounded-2xl border border-border bg-card shadow-sm">
        <CardHeader>
          <CardTitle className="text-lg">Arquivos inseridos</CardTitle>
          <CardDescription>Revise antes de enviar</CardDescription>
        </CardHeader>
        <Separator />
        <CardContent className="p-0">
          <ScrollArea className="h-[480px]">
            <ul className="p-3 space-y-2">
              {files.map((f, idx) => (
                <li
                  key={`${f.name}-${f.size}-${idx}`}
                  className={cn(
                    "flex items-center gap-3 rounded-xl border border-border px-3 py-2",
                    "bg-muted/40 hover:bg-muted/60 transition-colors"
                  )}
                >
                  <FileText className="h-4 w-4 text-muted-foreground shrink-0" />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium truncate">{f.name}</p>
                    <p className="text-xs text-muted-foreground">
                      {fmtBytes(f.size)}
                    </p>
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={() => handleRemoveAt(idx)}
                    disabled={uploadMutation.isPending}
                    aria-label={`Remover ${f.name}`}
                    className="h-8 w-8"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </li>
              ))}
            </ul>
          </ScrollArea>
        </CardContent>
      </Card>
    </section>
  );
}
