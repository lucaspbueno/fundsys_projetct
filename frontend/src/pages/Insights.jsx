import { useState, useMemo, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  BarChart3,
  TrendingUp,
  DollarSign,
  Calendar,
  Filter,
  Download,
  RefreshCw,
  PieChart,
  Activity,
  Target,
  History,
  ArrowLeft,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useOverview, useIndexadores, useEvolucaoMensal } from "@/hooks/useAnalytics";
import { useFileAnalytics } from "@/hooks/useHistory";
import { useEnrichmentStatus, useEnrichPendingAtivos } from "@/hooks/useEnrichment";
import { useFundoDetalhes } from "@/hooks/useFundo";

export default function Insights() {
  const [searchParams] = useSearchParams();
  const selectedFileId = searchParams.get('file');
  const selectedFundoId = searchParams.get('fundo');
  
  const [filters, setFilters] = useState({
    dateFrom: "",
    dateTo: "",
    indexador: "",
    ativo: "",
  });
  
  const [appliedFilters, setAppliedFilters] = useState({});
  const [enrichedMode, setEnrichedMode] = useState(false);

  // Use fund-specific analytics if fund ID is provided, otherwise use general overview
  const { data: fundoData, isLoading: fundoLoading } = useFundoDetalhes(selectedFundoId);
  const { data: fileAnalyticsData, isLoading: fileAnalyticsLoading } = useFileAnalytics(selectedFileId);
  const { data: overviewData, isLoading: overviewLoading, refetch: refetchOverview } = useOverview(enrichedMode, selectedFundoId, appliedFilters);
  const { data: indexadoresData, isLoading: indexadoresLoading } = useIndexadores();
  const { data: evolucaoData, isLoading: evolucaoLoading } = useEvolucaoMensal(null, appliedFilters);
  
  // Calcular crescimento baseado na evolução mensal
  const crescimento = useMemo(() => {
    if (!evolucaoData?.evolucao || evolucaoData.evolucao.length < 2) {
      return 0;
    }
    
    // Mapear nomes dos meses para números para ordenação correta
    const mesesNomes = {
      "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, 
      "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8, 
      "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
    };
    
    // Ordenar meses por número (mais recente primeiro)
    const meses = [...evolucaoData.evolucao].sort((a, b) => {
      const numA = mesesNomes[a.mes] || 0;
      const numB = mesesNomes[b.mes] || 0;
      return numB - numA;
    });
    
    const mesAtual = meses[0];
    const mesAnterior = meses[1];
    
    if (!mesAnterior || mesAnterior.valor_total === 0) {
      return 0;
    }
    
    const crescimento = ((mesAtual.valor_total - mesAnterior.valor_total) / mesAnterior.valor_total) * 100;
    return Math.round(crescimento * 10) / 10; // Arredondar para 1 casa decimal
  }, [evolucaoData]);
  
  // Enrichment status and controls
  const { data: enrichmentStatus } = useEnrichmentStatus();
  const enrichPendingMutation = useEnrichPendingAtivos();

  // Use file-specific data if available, otherwise fall back to general overview
  const analyticsData = selectedFileId ? fileAnalyticsData : overviewData;
  const loading = selectedFileId ? fileAnalyticsLoading : (overviewLoading || indexadoresLoading || evolucaoLoading);

  function handleFilterChange(key, value) {
    setFilters(prev => ({ ...prev, [key]: value }));
  }

  function handleApplyFilters() {
    // Aplicar os filtros digitados
    setAppliedFilters({ ...filters });
  }

  function handleClearFilters() {
    setFilters({
      dateFrom: "",
      dateTo: "",
      indexador: "",
      ativo: "",
    });
    setAppliedFilters({});
  }

  function handleRefresh() {
    refetchOverview();
  }

  function handleExport() {
    // Implementar exportação de dados
    console.log("Exportando dados...");
  }

  function handleToggleEnrichedMode() {
    setEnrichedMode(!enrichedMode);
  }

  function handleEnrichPending() {
    enrichPendingMutation.mutate({ 
      limit: 50, 
      background: true 
    });
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100dvh-64px)]">
        <div className="flex items-center gap-4">
          <RefreshCw className="h-8 w-8 animate-spin text-primary" />
          <span className="text-xl font-medium text-foreground">Carregando insights...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 sm:space-y-8 p-4 sm:p-6 lg:p-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 sm:gap-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            {selectedFileId && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => window.history.back()}
                className="text-muted-foreground hover:text-foreground"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Voltar
              </Button>
            )}
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-foreground">
              {selectedFileId ? "Analytics do Arquivo" : "Insights do Fundo"}
            </h1>
          </div>
          <p className="text-base sm:text-lg text-muted-foreground mt-1 sm:mt-2">
            {selectedFileId 
              ? `Análises específicas do arquivo: ${analyticsData?.nome_arquivo || 'Carregando...'}`
              : "Análises e métricas dos dados de investimento"
            }
          </p>
          {selectedFileId && analyticsData?.data_envio && (
            <p className="text-sm text-muted-foreground mt-1">
              Enviado em: {new Date(analyticsData.data_envio).toLocaleDateString('pt-BR', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              })}
            </p>
          )}
        </div>
        <div className="flex flex-col sm:flex-row gap-2 sm:gap-4">
          {/* Toggle para dados enriquecidos */}
          <Button
            onClick={handleToggleEnrichedMode}
            variant={enrichedMode ? "default" : "outline"}
            className={cn(
              "transition-all duration-200",
              enrichedMode 
                ? "bg-success hover:bg-success/90 text-success-foreground" 
                : "border-success/20 text-success hover:bg-success/10 hover:border-success/30"
            )}
            size="sm"
          >
            <Target className="h-4 w-4 sm:h-5 sm:w-5 mr-2" />
            <span className="hidden sm:inline">
              {enrichedMode ? "Dados Enriquecidos" : "Dados Normais"}
            </span>
            <span className="sm:hidden">
              {enrichedMode ? "Enriquecidos" : "Normais"}
            </span>
          </Button>
          
          {/* Botão para enriquecer ativos pendentes */}
          {!selectedFileId && enrichmentStatus && enrichmentStatus.sem_enriquecimento > 0 && (
            <Button
              onClick={handleEnrichPending}
              disabled={enrichPendingMutation.isPending}
              variant="outline"
              className="border-warning/20 text-warning hover:bg-warning/10 hover:border-warning/30"
              size="sm"
            >
              <RefreshCw className={cn("h-4 w-4 sm:h-5 sm:w-5 mr-2", enrichPendingMutation.isPending && "animate-spin")} />
              <span className="hidden sm:inline">
                Enriquecer ({enrichmentStatus.sem_enriquecimento})
              </span>
              <span className="sm:hidden">
                Enriquecer
              </span>
            </Button>
          )}
          
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
          <Button
            onClick={handleExport}
            className="bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg hover:shadow-xl transition-all duration-200"
            size="sm"
          >
            <Download className="h-4 w-4 sm:h-5 sm:w-5 mr-2" />
            <span className="hidden sm:inline">Exportar</span>
            <span className="sm:hidden">Exportar</span>
          </Button>
        </div>
      </div>

      {/* Filtros */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 sm:gap-3 text-lg sm:text-xl font-bold text-foreground">
            <Filter className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
            Filtros
          </CardTitle>
        </CardHeader>
        <CardContent className="px-4 sm:px-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
            <div>
              <Label htmlFor="dateFrom" className="text-sm font-medium">
                Data Inicial
                {filters.dateFrom && filters.dateFrom !== appliedFilters.dateFrom && (
                  <span className="ml-2 text-xs text-warning">• Pendente</span>
                )}
              </Label>
              <Input
                id="dateFrom"
                type="date"
                value={filters.dateFrom}
                onChange={(e) => handleFilterChange("dateFrom", e.target.value)}
                className={`border-border/50 focus:border-primary focus:ring-primary/20 text-sm ${
                  filters.dateFrom && filters.dateFrom !== appliedFilters.dateFrom 
                    ? 'border-warning/50 bg-warning/5' 
                    : ''
                }`}
              />
            </div>
            <div>
              <Label htmlFor="dateTo" className="text-sm font-medium">
                Data Final
                {filters.dateTo && filters.dateTo !== appliedFilters.dateTo && (
                  <span className="ml-2 text-xs text-warning">• Pendente</span>
                )}
              </Label>
              <Input
                id="dateTo"
                type="date"
                value={filters.dateTo}
                onChange={(e) => handleFilterChange("dateTo", e.target.value)}
                className={`border-border/50 focus:border-primary focus:ring-primary/20 text-sm ${
                  filters.dateTo && filters.dateTo !== appliedFilters.dateTo 
                    ? 'border-warning/50 bg-warning/5' 
                    : ''
                }`}
              />
            </div>
            <div>
              <Label htmlFor="indexador" className="text-sm font-medium">
                Indexador
                {filters.indexador && filters.indexador !== appliedFilters.indexador && (
                  <span className="ml-2 text-xs text-warning">• Pendente</span>
                )}
              </Label>
              <Input
                id="indexador"
                placeholder="Ex: DI1, IAP, PRE"
                value={filters.indexador}
                onChange={(e) => handleFilterChange("indexador", e.target.value)}
                className={`border-border/50 focus:border-primary focus:ring-primary/20 text-sm ${
                  filters.indexador && filters.indexador !== appliedFilters.indexador 
                    ? 'border-warning/50 bg-warning/5' 
                    : ''
                }`}
              />
            </div>
            <div>
              <Label htmlFor="ativo" className="text-sm font-medium">
                Código do Ativo
                {filters.ativo && filters.ativo !== appliedFilters.ativo && (
                  <span className="ml-2 text-xs text-warning">• Pendente</span>
                )}
              </Label>
              <Input
                id="ativo"
                placeholder="Ex: CRA02300FFL"
                value={filters.ativo}
                onChange={(e) => handleFilterChange("ativo", e.target.value)}
                className={`border-border/50 focus:border-primary focus:ring-primary/20 text-sm ${
                  filters.ativo && filters.ativo !== appliedFilters.ativo 
                    ? 'border-warning/50 bg-warning/5' 
                    : ''
                }`}
              />
            </div>
          </div>
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-4 mt-4">
            <Button
              onClick={handleApplyFilters}
              className="bg-primary hover:bg-primary/90 text-primary-foreground"
              size="sm"
            >
              <Filter className="h-4 w-4 mr-2" />
              Aplicar Filtros
            </Button>
            <Button
              onClick={handleClearFilters}
              variant="outline"
              className="border-muted-foreground/20 text-muted-foreground hover:bg-muted/10"
              size="sm"
            >
              Limpar Filtros
            </Button>
            {Object.keys(appliedFilters).some(key => appliedFilters[key]) && (
              <div className="flex items-center gap-2 text-sm text-success">
                <div className="w-2 h-2 bg-success rounded-full"></div>
                Filtros aplicados
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Métricas Principais */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <Card className="border-success/20 bg-success/5 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300">
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs sm:text-sm font-medium text-success">Total de Ativos</p>
                <p className="text-2xl sm:text-3xl font-bold text-foreground">
                  {analyticsData?.total_ativos || 0}
                </p>
              </div>
              <BarChart3 className="h-6 w-6 sm:h-8 sm:w-8 text-success" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-info/20 bg-info/5 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300">
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs sm:text-sm font-medium text-info">Valor Total</p>
                <p className="text-lg sm:text-2xl lg:text-3xl font-bold text-foreground">
                  R$ {(analyticsData?.valor_total || 0).toLocaleString('pt-BR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  })}
                </p>
              </div>
              <DollarSign className="h-6 w-6 sm:h-8 sm:w-8 text-info" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-purple/20 bg-purple/5 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300">
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs sm:text-sm font-medium text-purple">Indexadores</p>
                <p className="text-2xl sm:text-3xl font-bold text-foreground">
                  {analyticsData?.total_indexadores || 0}
                </p>
              </div>
              <PieChart className="h-6 w-6 sm:h-8 sm:w-8 text-purple" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-warning/20 bg-warning/5 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300">
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs sm:text-sm font-medium text-warning">Crescimento</p>
                <p className="text-2xl sm:text-3xl font-bold text-foreground">
                  {crescimento > 0 ? '+' : ''}{crescimento}%
                </p>
              </div>
              <TrendingUp className="h-6 w-6 sm:h-8 sm:w-8 text-warning" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos e Análises */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        {/* Distribuição por Indexador */}
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-2 sm:gap-3 text-lg sm:text-xl font-bold text-foreground">
              <PieChart className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
              Distribuição por Indexador
            </CardTitle>
          </CardHeader>
          <CardContent className="px-4 sm:px-6">
            <div className="space-y-3 sm:space-y-4">
              {analyticsData?.indexadores?.map((item, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm sm:text-base font-medium text-foreground">{item.nome || 'N/A'}</span>
                    <span className="text-xs sm:text-sm text-muted-foreground">
                      {item.quantidade || 0} ativos ({(item.percentual || 0).toFixed(1)}%)
                    </span>
                  </div>
                  <div className="w-full bg-muted/30 rounded-full h-2 sm:h-3">
                    <div
                      className={cn(
                        "h-2 sm:h-3 rounded-full transition-all duration-500",
                        index === 0 && "bg-success",
                        index === 1 && "bg-info",
                        index === 2 && "bg-purple"
                      )}
                      style={{ width: `${item.percentual || 0}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Top Ativos */}
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-2 sm:gap-3 text-lg sm:text-xl font-bold text-foreground">
              <Target className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
              Top Ativos por Valor
            </CardTitle>
          </CardHeader>
          <CardContent className="px-4 sm:px-6">
            <div className="space-y-3 sm:space-y-4">
              {analyticsData?.top_ativos?.map((ativo, index) => (
                <div key={index} className="flex items-center justify-between p-3 sm:p-4 bg-muted/20 hover:bg-muted/30 rounded-lg sm:rounded-xl transition-all duration-200">
                  <div className="flex-1">
                    <p className="text-sm sm:text-base font-medium text-foreground">{ativo.codigo || 'N/A'}</p>
                    <p className="text-xs sm:text-sm text-muted-foreground">{ativo.indexador || 'N/A'}</p>
                    
                    {/* Dados enriquecidos */}
                    {enrichedMode && (ativo.serie || ativo.emissao || ativo.devedor || ativo.securitizadora) && (
                      <div className="mt-2 space-y-1">
                        {ativo.serie && (
                          <p className="text-xs text-success">
                            <span className="font-medium">Série:</span> {ativo.serie || 'N/A'}
                          </p>
                        )}
                        {ativo.emissao && (
                          <p className="text-xs text-success">
                            <span className="font-medium">Emissão:</span> {ativo.emissao || 'N/A'}
                          </p>
                        )}
                        {ativo.devedor && (
                          <p className="text-xs text-success">
                            <span className="font-medium">Devedor:</span> {ativo.devedor || 'N/A'}
                          </p>
                        )}
                        {ativo.securitizadora && (
                          <p className="text-xs text-success">
                            <span className="font-medium">Securitizadora:</span> {ativo.securitizadora || 'N/A'}
                          </p>
                        )}
                        {ativo.resgate_antecipado !== null && (
                          <p className="text-xs text-success">
                            <span className="font-medium">Resgate Antecipado:</span> {ativo.resgate_antecipado ? "Sim" : "Não"}
                          </p>
                        )}
                        {ativo.agente_fiduciario && (
                          <p className="text-xs text-success">
                            <span className="font-medium">Agente Fiduciário:</span> {ativo.agente_fiduciario}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                  <div className="text-right">
                    <p className="text-sm sm:text-base font-bold text-primary">
                      R$ {(ativo.valor || 0).toLocaleString('pt-BR', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                      })}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Gráfico de Evolução Mensal */}
      <Card className="border-border/50 bg-card/50 backdrop-blur-sm shadow-lg">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 sm:gap-3 text-lg sm:text-xl font-bold text-foreground">
            <Activity className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
            Evolução Mensal
          </CardTitle>
          <CardDescription className="text-sm sm:text-base text-muted-foreground">
            Quantidade de ativos e valor total por mês
          </CardDescription>
        </CardHeader>
        <CardContent className="px-4 sm:px-6">
          <div className="space-y-3 sm:space-y-4">
            {evolucaoData?.evolucao?.map((mes, index) => (
              <div key={index} className="flex flex-col sm:flex-row sm:items-center justify-between p-4 sm:p-6 bg-gradient-to-r from-primary/5 to-primary/10 rounded-xl sm:rounded-2xl hover:from-primary/10 hover:to-primary/15 transition-all duration-300 gap-3 sm:gap-4">
                <div className="flex items-center gap-3 sm:gap-4">
                  <div className="w-10 h-10 sm:w-14 sm:h-14 bg-primary/10 rounded-xl sm:rounded-2xl flex items-center justify-center">
                    <Calendar className="h-5 w-5 sm:h-7 sm:w-7 text-primary" />
                  </div>
                  <div>
                    <p className="font-bold text-lg sm:text-xl text-foreground">{mes.mes || 'N/A'}</p>
                    <p className="text-xs sm:text-sm text-muted-foreground">{mes.quantidade || 0} ativos</p>
                  </div>
                </div>
                <div className="text-left sm:text-right">
                  <p className="text-lg sm:text-2xl font-bold text-primary">
                    R$ {(mes.valor_total || 0).toLocaleString('pt-BR')}
                  </p>
                  <p className="text-xs sm:text-sm text-muted-foreground">Valor total</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
