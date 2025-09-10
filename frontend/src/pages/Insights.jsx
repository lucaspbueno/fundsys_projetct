import { useState, useMemo } from "react";
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
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useOverview, useIndexadores, useEvolucaoMensal } from "@/hooks/useAnalytics";

export default function Insights() {
  const [filters, setFilters] = useState({
    dateFrom: "",
    dateTo: "",
    indexador: "",
    ativo: "",
  });

  // Buscar dados da API
  const { data: overviewData, isLoading: overviewLoading, refetch: refetchOverview } = useOverview();
  const { data: indexadoresData, isLoading: indexadoresLoading } = useIndexadores();
  const { data: evolucaoData, isLoading: evolucaoLoading } = useEvolucaoMensal();

  const loading = overviewLoading || indexadoresLoading || evolucaoLoading;

  function handleFilterChange(key, value) {
    setFilters(prev => ({ ...prev, [key]: value }));
  }

  function handleRefresh() {
    refetchOverview();
  }

  function handleExport() {
    // Implementar exportação de dados
    console.log("Exportando dados...");
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
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-foreground">
            Insights do Fundo
          </h1>
          <p className="text-base sm:text-lg text-muted-foreground mt-1 sm:mt-2">
            Análises e métricas dos dados de investimento
          </p>
        </div>
        <div className="flex flex-col sm:flex-row gap-2 sm:gap-4">
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
              <Label htmlFor="dateFrom" className="text-sm font-medium">Data Inicial</Label>
              <Input
                id="dateFrom"
                type="date"
                value={filters.dateFrom}
                onChange={(e) => handleFilterChange("dateFrom", e.target.value)}
                className="border-border/50 focus:border-primary focus:ring-primary/20 text-sm"
              />
            </div>
            <div>
              <Label htmlFor="dateTo" className="text-sm font-medium">Data Final</Label>
              <Input
                id="dateTo"
                type="date"
                value={filters.dateTo}
                onChange={(e) => handleFilterChange("dateTo", e.target.value)}
                className="border-border/50 focus:border-primary focus:ring-primary/20 text-sm"
              />
            </div>
            <div>
              <Label htmlFor="indexador" className="text-sm font-medium">Indexador</Label>
              <Input
                id="indexador"
                placeholder="Ex: DI1, IAP, PRE"
                value={filters.indexador}
                onChange={(e) => handleFilterChange("indexador", e.target.value)}
                className="border-border/50 focus:border-primary focus:ring-primary/20 text-sm"
              />
            </div>
            <div>
              <Label htmlFor="ativo" className="text-sm font-medium">Código do Ativo</Label>
              <Input
                id="ativo"
                placeholder="Ex: CRA02300FFL"
                value={filters.ativo}
                onChange={(e) => handleFilterChange("ativo", e.target.value)}
                className="border-border/50 focus:border-primary focus:ring-primary/20 text-sm"
              />
            </div>
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
                  {overviewData?.total_ativos || 0}
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
                  R$ {(overviewData?.valor_total || 0).toLocaleString('pt-BR', {
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
                  {overviewData?.total_indexadores || 0}
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
                <p className="text-2xl sm:text-3xl font-bold text-foreground">+12.5%</p>
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
              {overviewData?.indexadores?.map((item, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm sm:text-base font-medium text-foreground">{item.nome}</span>
                    <span className="text-xs sm:text-sm text-muted-foreground">
                      {item.quantidade} ativos ({item.percentual}%)
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
                      style={{ width: `${item.percentual}%` }}
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
              {overviewData?.top_ativos?.map((ativo, index) => (
                <div key={index} className="flex items-center justify-between p-3 sm:p-4 bg-muted/20 hover:bg-muted/30 rounded-lg sm:rounded-xl transition-all duration-200">
                  <div>
                    <p className="text-sm sm:text-base font-medium text-foreground">{ativo.codigo}</p>
                    <p className="text-xs sm:text-sm text-muted-foreground">{ativo.indexador}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm sm:text-base font-bold text-primary">
                      R$ {ativo.valor.toLocaleString('pt-BR', {
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
                    <p className="font-bold text-lg sm:text-xl text-foreground">{mes.mes}</p>
                    <p className="text-xs sm:text-sm text-muted-foreground">{mes.quantidade} ativos</p>
                  </div>
                </div>
                <div className="text-left sm:text-right">
                  <p className="text-lg sm:text-2xl font-bold text-primary">
                    R$ {mes.valor.toLocaleString('pt-BR')}
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
