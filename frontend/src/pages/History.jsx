import { useState } from "react";
import {
  Card, CardHeader, CardTitle, CardDescription, CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import {
  History as HistoryIcon, FileText, Calendar, DollarSign, BarChart3, Eye, RefreshCw, Search, Filter
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useFileHistory } from "@/hooks/useHistory";

export default function History() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [pagination, setPagination] = useState({ limit: 10, offset: 0 });

  const { data: historyData, isLoading, refetch } = useFileHistory(pagination.limit, pagination.offset);

  const handleSearch = (value) => {
    setSearchTerm(value);
    // Reset pagination when searching
    setPagination({ limit: 10, offset: 0 });
  };

  const handleFileSelect = (file) => {
    setSelectedFile(file);
  };

  const handleViewAnalytics = (file) => {
    // Navigate to insights with selected file
    window.location.href = `/insights?file=${file.id_lote}`;
  };

  const handleLoadMore = () => {
    setPagination(prev => ({
      ...prev,
      offset: prev.offset + prev.limit
    }));
  };

  const handleRefresh = () => {
    refetch();
  };

  // Filter files based on search term
  const filteredFiles = historyData?.files?.filter(file =>
    file.nome_arquivo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    file.indexadores.some(idx => idx.toLowerCase().includes(searchTerm.toLowerCase()))
  ) || [];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100dvh-64px)]">
        <div className="flex items-center gap-4">
          <RefreshCw className="h-8 w-8 animate-spin text-primary" />
          <span className="text-xl font-medium text-foreground">Carregando histórico...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 sm:space-y-8 p-4 sm:p-6 lg:p-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 sm:gap-6">
        <div>
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-foreground">
            Histórico de Arquivos
          </h1>
          <p className="text-base sm:text-lg text-muted-foreground mt-1 sm:mt-2">
            Visualize e gerencie arquivos enviados anteriormente
          </p>
        </div>
        <div className="flex gap-2 sm:gap-4">
          <Button
            onClick={handleRefresh}
            variant="outline"
            className="border-primary/20 text-primary hover:bg-primary/10 hover:border-primary/30"
            size="sm"
          >
            <RefreshCw className="h-4 w-4 sm:h-5 sm:w-5 mr-2" />
            <span className="hidden sm:inline">Atualizar</span>
            <span className="sm:hidden">Atualizar</span>
          </Button>
        </div>
      </div>

      {/* Search and Filters */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 sm:gap-3 text-lg sm:text-xl font-bold text-foreground">
            <Search className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
            Buscar Arquivos
          </CardTitle>
        </CardHeader>
        <CardContent className="px-4 sm:px-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <Label htmlFor="search" className="text-sm font-medium">Nome do arquivo ou indexador</Label>
              <Input
                id="search"
                placeholder="Ex: dados_fundo.xml ou DI1"
                value={searchTerm}
                onChange={(e) => handleSearch(e.target.value)}
                className="border-border/50 focus:border-primary focus:ring-primary/20 text-sm"
              />
            </div>
            <div className="flex items-end">
              <Button
                variant="outline"
                onClick={() => setSearchTerm("")}
                className="border-primary/20 text-primary hover:bg-primary/10 hover:border-primary/30"
                size="sm"
              >
                Limpar
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Files List */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
        {/* Files List */}
        <div className="lg:col-span-2">
          <Card className="border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-2 sm:gap-3 text-lg sm:text-xl font-bold text-foreground">
                <FileText className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
                Arquivos Enviados ({filteredFiles.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <ScrollArea className="h-[600px] sm:h-[700px]">
                <div className="p-4 sm:p-6 space-y-3 sm:space-y-4">
                  {filteredFiles.length === 0 ? (
                    <div className="text-center py-8">
                      <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <p className="text-muted-foreground">
                        {searchTerm ? "Nenhum arquivo encontrado" : "Nenhum arquivo enviado ainda"}
                      </p>
                    </div>
                  ) : (
                    filteredFiles.map((file) => (
                      <Card
                        key={file.id_lote}
                        className={cn(
                          "border-border/50 bg-card/50 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer",
                          selectedFile?.id_lote === file.id_lote && "ring-2 ring-primary/50 bg-primary/5"
                        )}
                        onClick={() => handleFileSelect(file)}
                      >
                        <CardContent className="p-4 sm:p-6">
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-2">
                                <FileText className="h-4 w-4 text-primary flex-shrink-0" />
                                <h3 className="font-semibold text-foreground truncate">
                                  {file.nome_arquivo}
                                </h3>
                              </div>
                              
                              <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mb-3">
                                <div className="flex items-center gap-1">
                                  <Calendar className="h-3 w-3" />
                                  <span>
                                    {new Date(file.data_envio).toLocaleDateString('pt-BR', {
                                      day: '2-digit',
                                      month: '2-digit',
                                      year: 'numeric',
                                      hour: '2-digit',
                                      minute: '2-digit'
                                    })}
                                  </span>
                                </div>
                                <div className="flex items-center gap-1">
                                  <BarChart3 className="h-3 w-3" />
                                  <span>{file.quantidade_ativos} ativos</span>
                                </div>
                                <div className="flex items-center gap-1">
                                  <DollarSign className="h-3 w-3" />
                                  <span>
                                    R$ {file.valor_total.toLocaleString('pt-BR', {
                                      minimumFractionDigits: 2,
                                      maximumFractionDigits: 2
                                    })}
                                  </span>
                                </div>
                              </div>

                              <div className="flex flex-wrap gap-1">
                                {file.indexadores.slice(0, 3).map((indexador, idx) => (
                                  <span
                                    key={idx}
                                    className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary"
                                  >
                                    {indexador}
                                  </span>
                                ))}
                                {file.indexadores.length > 3 && (
                                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-muted text-muted-foreground">
                                    +{file.indexadores.length - 3} mais
                                  </span>
                                )}
                              </div>
                            </div>

                            <div className="flex flex-col gap-2">
                              <Button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleViewAnalytics(file);
                                }}
                                className="bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg hover:shadow-xl transition-all duration-200"
                                size="sm"
                              >
                                <Eye className="h-4 w-4 mr-2" />
                                Ver Analytics
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))
                  )}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>

          {/* Load More Button */}
          {historyData && filteredFiles.length < historyData.total && (
            <div className="mt-4 text-center">
              <Button
                onClick={handleLoadMore}
                variant="outline"
                className="border-primary/20 text-primary hover:bg-primary/10 hover:border-primary/30"
              >
                Carregar Mais
              </Button>
            </div>
          )}
        </div>

        {/* File Details */}
        <div className="lg:col-span-1">
          <Card className="border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
            <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-2 sm:gap-3 text-lg sm:text-xl font-bold text-foreground">
              <HistoryIcon className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
              Detalhes do Arquivo
            </CardTitle>
            </CardHeader>
            <CardContent className="px-4 sm:px-6">
              {selectedFile ? (
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-foreground mb-2">{selectedFile.nome_arquivo}</h3>
                    <p className="text-sm text-muted-foreground">
                      Enviado em {new Date(selectedFile.data_envio).toLocaleDateString('pt-BR', {
                        day: '2-digit',
                        month: '2-digit',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </p>
                  </div>

                  <Separator className="bg-border/50" />

                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-muted-foreground">Total de Ativos</span>
                      <span className="text-lg font-bold text-foreground">{selectedFile.quantidade_ativos}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-muted-foreground">Valor Total</span>
                      <span className="text-lg font-bold text-primary">
                        R$ {selectedFile.valor_total.toLocaleString('pt-BR', {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2
                        })}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-muted-foreground">Indexadores</span>
                      <span className="text-lg font-bold text-foreground">{selectedFile.indexadores.length}</span>
                    </div>
                  </div>

                  <Separator className="bg-border/50" />

                  <div>
                    <h4 className="text-sm font-medium text-foreground mb-2">Indexadores</h4>
                    <div className="flex flex-wrap gap-1">
                      {selectedFile.indexadores.map((indexador, idx) => (
                        <span
                          key={idx}
                          className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary"
                        >
                          {indexador}
                        </span>
                      ))}
                    </div>
                  </div>

                  <Button
                    onClick={() => handleViewAnalytics(selectedFile)}
                    className="w-full bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg hover:shadow-xl transition-all duration-200"
                  >
                    <Eye className="h-4 w-4 mr-2" />
                    Ver Analytics Detalhadas
                  </Button>
                </div>
              ) : (
                <div className="text-center py-8">
                  <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">
                    Selecione um arquivo para ver os detalhes
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
