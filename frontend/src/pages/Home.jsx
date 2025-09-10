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
        <div className="flex items-center gap-4 p-6 rounded-2xl bg-primary/5 border border-primary/20 text-primary">
          <CheckCircle className="h-6 w-6 text-primary flex-shrink-0" />
          <div className="flex-1">
            <p className="font-semibold text-base">Upload realizado com sucesso!</p>
            <p className="text-sm text-primary/80 mt-1">
              {uploadResult?.qtd_arquivos_processados} arquivo(s) processado(s) e {uploadResult?.data?.length || 0} registro(s) inserido(s) no banco.
            </p>
          </div>
        </div>
      );
    }

    if (uploadStatus === 'error') {
      return (
        <div className="flex items-center gap-4 p-6 rounded-2xl bg-destructive/5 border border-destructive/20 text-destructive">
          <AlertCircle className="h-6 w-6 text-destructive flex-shrink-0" />
          <div className="flex-1">
            <p className="font-semibold text-base">Erro no upload</p>
            <p className="text-sm text-destructive/80 mt-1">
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
      <section className="grid place-items-center min-h-[calc(100dvh-64px)] p-4 sm:p-6">
        <Card className="w-full max-w-2xl sm:max-w-4xl rounded-2xl sm:rounded-3xl border border-border/50 bg-card/50 backdrop-blur-sm shadow-xl">
          <CardHeader className="text-center pb-6 sm:pb-8 px-4 sm:px-6">
            <CardTitle className="text-2xl sm:text-3xl font-bold text-foreground">
              Importar XML
            </CardTitle>
            <CardDescription className="text-base sm:text-lg text-muted-foreground">
              Arraste o arquivo .xml ou clique para selecionar
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-6 sm:space-y-8 px-4 sm:px-6">
            <Dropzone onFiles={handleAddFiles} disabled={isUploading} />

            <UploadStatus />

            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
              <Button
                onClick={handleProcess}
                disabled={!hasFiles || isUploading}
                className="w-full sm:w-auto bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg hover:shadow-xl transition-all duration-200"
                size="lg"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 sm:h-5 sm:w-5 animate-spin" />
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
                className="w-full sm:w-auto border-primary/20 text-primary hover:bg-primary/10 hover:border-primary/30"
                size="lg"
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
        "mx-auto w-full p-4 sm:p-6",
        "grid gap-6 sm:gap-8",
        // em telas grandes vira duas colunas: conteúdo | painel de arquivos
        "lg:grid-cols-[minmax(0,1fr)_400px] xl:grid-cols-[minmax(0,1fr)_480px]"
      )}
    >
      {/* Coluna esquerda: card com dropzone + ações */}
      <Card className="rounded-2xl sm:rounded-3xl border border-border/50 bg-card/50 backdrop-blur-sm shadow-xl">
        <CardHeader className="text-center pb-4 sm:pb-6 px-4 sm:px-6">
          <CardTitle className="text-xl sm:text-2xl font-bold text-foreground">
            Importar XML
          </CardTitle>
          <CardDescription className="text-sm sm:text-base text-muted-foreground">
            Arraste os arquivos .xml ou clique para selecionar
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4 sm:space-y-6 px-4 sm:px-6">
          <Dropzone onFiles={handleAddFiles} disabled={isUploading} />

          <div className="flex items-center justify-between text-xs sm:text-sm text-muted-foreground bg-muted/30 rounded-lg px-3 sm:px-4 py-2">
            <span className="font-medium">{files.length} arquivo(s)</span>
            <span className="font-mono">{fmtBytes(totalSize)}</span>
          </div>

          <UploadStatus />

          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
            <Button
              onClick={handleProcess}
              disabled={!hasFiles || isUploading}
              className="w-full sm:w-auto bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg hover:shadow-xl transition-all duration-200"
              size="lg"
            >
              {isUploading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 sm:h-5 sm:w-5 animate-spin" />
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
              className="w-full sm:w-auto border-primary/20 text-primary hover:bg-primary/10 hover:border-primary/30"
              size="lg"
            >
              Limpar
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Coluna direita: painel com lista de arquivos */}
      <Card className="rounded-2xl sm:rounded-3xl border border-border/50 bg-card/50 backdrop-blur-sm shadow-xl">
        <CardHeader className="pb-3 sm:pb-4 px-4 sm:px-6">
          <CardTitle className="text-lg sm:text-xl font-bold text-foreground">Arquivos inseridos</CardTitle>
          <CardDescription className="text-sm sm:text-base text-muted-foreground">Revise antes de enviar</CardDescription>
        </CardHeader>
        <Separator className="bg-border/50" />
        <CardContent className="p-0">
          <ScrollArea className="h-[400px] sm:h-[520px]">
            <ul className="p-3 sm:p-4 space-y-2 sm:space-y-3">
              {files.map((f, idx) => (
                <li
                  key={`${f.name}-${f.size}-${idx}`}
                  className={cn(
                    "flex items-center gap-3 sm:gap-4 rounded-lg sm:rounded-xl border border-border/50 px-3 sm:px-4 py-2 sm:py-3",
                    "bg-muted/20 hover:bg-muted/40 transition-all duration-200 hover:scale-[1.01] sm:hover:scale-[1.02]"
                  )}
                >
                  <FileText className="h-4 w-4 sm:h-5 sm:w-5 text-primary/70 shrink-0" />
                  <div className="min-w-0 flex-1">
                    <p className="text-xs sm:text-sm font-medium truncate text-foreground">{f.name}</p>
                    <p className="text-xs text-muted-foreground font-mono">
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
                    className="h-7 w-7 sm:h-8 sm:w-8 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                  >
                    <Trash2 className="h-3 w-3 sm:h-4 sm:w-4" />
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
