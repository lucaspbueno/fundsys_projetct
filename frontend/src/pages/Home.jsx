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
import { FileText, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";

export default function Home() {
  const [files, setFiles] = useState([]);

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

  const totalSize = useMemo(
    () => files.reduce((acc, f) => acc + (f?.size || 0), 0),
    [files]
  );

  function fmtBytes(n) {
    if (!n) return "0 B";
    const k = 1024;
    const units = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(n) / Math.log(k));
    return `${(n / Math.pow(k, i)).toFixed(i ? 1 : 0)} ${units[i]}`;
    }

  function handleProcess() {
    if (!hasFiles) return;
    // Exemplo: enviar via FormData (multi-arquivo)
    // const fd = new FormData();
    // files.forEach((f) => fd.append("files", f));
    // await api.post("/upload", fd);
    console.log("Pronto para enviar:", files);
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
            <Dropzone onFiles={handleAddFiles} />

            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Button onClick={handleProcess} disabled={!hasFiles} className="w-full sm:w-auto">
                Enviar XML
              </Button>
              <Button variant="outline" onClick={handleClear} className="w-full sm:w-auto">
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
          <Dropzone onFiles={handleAddFiles} />

          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>{files.length} arquivo(s)</span>
            <span>{fmtBytes(totalSize)}</span>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Button onClick={handleProcess} disabled={!hasFiles} className="w-full sm:w-auto">
              Enviar XML
            </Button>
            <Button variant="outline" onClick={handleClear} className="w-full sm:w-auto">
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
                    <p className="text-xs text-muted-foreground">{fmtBytes(f.size)}</p>
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={() => handleRemoveAt(idx)}
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
