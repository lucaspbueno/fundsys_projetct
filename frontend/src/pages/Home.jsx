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
import { useUploadFundo } from "@/hooks/useFundo";
import { SuccessModal, ErrorModal, WarningModal } from "@/components/ui/modal";
import { usePageTitle } from "@/hooks/usePageTitle";

export default function Home() {
  const [files, setFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState(null); // 'success', 'error', null
  const [uploadResult, setUploadResult] = useState(null);
  const uploadMutation = useUploadFundo();
  
  // Definir título e ícone da página
  usePageTitle("FundSys - Upload de Arquivos", "/icons/fundsys-light.svg");
  const [modalState, setModalState] = useState({
    isOpen: false,
    type: null, // 'success', 'error', 'warning'
    title: '',
    message: '',
    fundoId: null
  });

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
          <div>
            <p className="font-semibold text-base">Upload realizado com sucesso!</p>
            <p className="text-sm opacity-90">
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
          <div>
            <p className="font-semibold text-base">Erro no upload</p>
            <p className="text-sm opacity-90">{uploadResult}</p>
          </div>
        </div>
      );
    }

    return null;
  }

  function fmtBytes(n) {
    if (n === 0) return "0 B";
    const k = 1024;
    const units = ["B", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(n) / Math.log(k));
    return `${(n / Math.pow(k, i)).toFixed(i ? 1 : 0)} ${units[i]}`;
  }

  function handleProcess() {
    if (!hasFiles || uploadMutation.isPending) return;
    
    setUploadStatus(null);
    setUploadResult(null);
    
    // Processar apenas o primeiro arquivo (um fundo por arquivo)
    const arquivo = files[0];
    
    uploadMutation.mutate(arquivo, {
      onSuccess: (data) => {
        if (data.sucesso) {
          setUploadStatus('success');
          setUploadResult(data);
          handleClear();
          
          setModalState({
            isOpen: true,
            type: 'success',
            title: 'Fundo Criado com Sucesso!',
            message: `O fundo foi criado com sucesso. Você pode visualizar suas análises na tela de Insights.`,
            fundoId: data.fundo_id
          });
        } else {
          if (data.arquivo_duplicado) {
            setModalState({
              isOpen: true,
              type: 'warning',
              title: 'Arquivo Já Analisado',
              message: data.mensagem,
              fundoId: data.fundo_existente?.id_fundo_investimento
            });
          } else {
            setModalState({
              isOpen: true,
              type: 'error',
              title: 'Erro no Upload',
              message: data.mensagem
            });
          }
        }
      },
      onError: (err) => {
        setUploadStatus('error');
        const msg =
          err?.response?.data?.detail ||
          err?.response?.data?.message ||
          err?.message ||
          "Erro ao enviar arquivo. Tente novamente.";
        
        setModalState({
          isOpen: true,
          type: 'error',
          title: 'Erro no Upload',
          message: msg
        });
      },
    });
  }

  // Função para fechar modal
  function closeModal() {
    setModalState({
      isOpen: false,
      type: null,
      title: '',
      message: '',
      fundoId: null
    });
  }

  // Função para navegar para analytics
  function goToAnalytics() {
    if (modalState.fundoId) {
      window.location.href = `/insights?fundo=${modalState.fundoId}`;
    } else {
      window.location.href = '/insights';
    }
  }

  return (
    <>
      {/* Conteúdo principal */}
      {!hasFiles ? (
        // estado vazio — tela centralizada
        <section className="mx-auto w-full max-w-4xl p-4 sm:p-6">
          <Card className="rounded-2xl sm:rounded-3xl border border-border/50 bg-card/50 backdrop-blur-sm shadow-xl">
            <CardHeader className="text-center pb-4 sm:pb-6 px-4 sm:px-6">
              <CardTitle className="text-xl sm:text-2xl font-bold text-foreground">
                Importar XML
              </CardTitle>
              <CardDescription className="text-sm sm:text-base text-muted-foreground">
                Arraste o arquivo .xml ou clique para selecionar
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4 sm:space-y-6 px-4 sm:px-6">
              <Dropzone onFiles={handleAddFiles} disabled={isUploading} />
              <UploadStatus />
            </CardContent>
          </Card>
        </section>
      ) : (
        // estado com arquivos — layout split
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
              <UploadStatus />
              
              <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
                <Button
                  onClick={handleProcess}
                  disabled={!hasFiles || isUploading}
                  className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg hover:shadow-xl transition-all duration-200"
                  size="lg"
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="h-4 w-4 sm:h-5 sm:w-5 mr-2 animate-spin" />
                      <span className="hidden sm:inline">Processando...</span>
                      <span className="sm:hidden">Processando...</span>
                    </>
                  ) : (
                    <>
                      <FileText className="h-4 w-4 sm:h-5 sm:w-5 mr-2" />
                      <span className="hidden sm:inline">Processar Arquivo</span>
                      <span className="sm:hidden">Processar</span>
                    </>
                  )}
                </Button>
                <Button
                  onClick={handleClear}
                  variant="outline"
                  disabled={isUploading}
                  className="border-border/50 text-muted-foreground hover:text-foreground hover:bg-muted/50"
                  size="lg"
                >
                  <Trash2 className="h-4 w-4 sm:h-5 sm:w-5 mr-2" />
                  <span className="hidden sm:inline">Limpar</span>
                  <span className="sm:hidden">Limpar</span>
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Coluna direita: lista de arquivos */}
          <Card className="rounded-2xl sm:rounded-3xl border border-border/50 bg-card/50 backdrop-blur-sm shadow-xl">
            <CardHeader className="pb-4 px-4 sm:px-6">
              <CardTitle className="flex items-center gap-2 sm:gap-3 text-lg sm:text-xl font-bold text-foreground">
                <FileText className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
                Arquivo Selecionado
                <span className="text-sm font-normal text-muted-foreground">
                  ({files.length})
                </span>
              </CardTitle>
              <CardDescription className="text-sm text-muted-foreground">
                {fmtBytes(totalSize)} total
              </CardDescription>
            </CardHeader>

            <CardContent className="px-4 sm:px-6">
              <ScrollArea className="h-[300px] sm:h-[400px]">
                <ul className="space-y-2 sm:space-y-3">
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
      )}
      
      {/* Modais */}
      {modalState.type === 'success' && (
        <SuccessModal
          isOpen={modalState.isOpen}
          onClose={closeModal}
          title={modalState.title}
          message={modalState.message}
          actionLabel="Ver Análises"
          onAction={goToAnalytics}
        />
      )}
      
      {modalState.type === 'error' && (
        <ErrorModal
          isOpen={modalState.isOpen}
          onClose={closeModal}
          title={modalState.title}
          message={modalState.message}
        />
      )}
      
      {modalState.type === 'warning' && (
        <WarningModal
          isOpen={modalState.isOpen}
          onClose={closeModal}
          title={modalState.title}
          message={modalState.message}
          actionLabel="Ver Análises"
          onAction={goToAnalytics}
        />
      )}
    </>
  );
}

