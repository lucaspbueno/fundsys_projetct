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
      <div className="flex items-center justify-center min-h-[calc(100dvh-56px)]">
        <div className="flex items-center gap-3">
          <RefreshCw className="h-6 w-6 animate-spin text-green-600 dark:text-green-400" />
          <span className="text-lg text-foreground">Carregando insights...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Insights do Fundo</h1>
          <p className="text-muted-foreground mt-1">
            Análises e métricas dos dados de investimento
          </p>
        </div>
        <div className="flex gap-3">
          <Button
            onClick={handleRefresh}
            variant="outline"
            className="border-green-200 dark:border-green-800 text-green-700 dark:text-green-300 hover:bg-green-50 dark:hover:bg-green-900/20"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Atualizar
          </Button>
          <Button
            onClick={handleExport}
            className="bg-green-600 hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-600 text-white"
          >
            <Download className="h-4 w-4 mr-2" />
            Exportar
          </Button>
        </div>
      </div>

      {/* Filtros */}
      <Card className="border-green-200 dark:border-green-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-800 dark:text-green-300">
            <Filter className="h-5 w-5" />
            Filtros
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <Label htmlFor="dateFrom">Data Inicial</Label>
              <Input
                id="dateFrom"
                type="date"
                value={filters.dateFrom}
                onChange={(e) => handleFilterChange("dateFrom", e.target.value)}
                className="border-green-200 dark:border-green-800 focus:border-green-500 dark:focus:border-green-400"
              />
            </div>
            <div>
              <Label htmlFor="dateTo">Data Final</Label>
              <Input
                id="dateTo"
                type="date"
                value={filters.dateTo}
                onChange={(e) => handleFilterChange("dateTo", e.target.value)}
                className="border-green-200 dark:border-green-800 focus:border-green-500 dark:focus:border-green-400"
              />
            </div>
            <div>
              <Label htmlFor="indexador">Indexador</Label>
              <Input
                id="indexador"
                placeholder="Ex: DI1, IAP, PRE"
                value={filters.indexador}
                onChange={(e) => handleFilterChange("indexador", e.target.value)}
                className="border-green-200 dark:border-green-800 focus:border-green-500 dark:focus:border-green-400"
              />
            </div>
            <div>
              <Label htmlFor="ativo">Código do Ativo</Label>
              <Input
                id="ativo"
                placeholder="Ex: CRA02300FFL"
                value={filters.ativo}
                onChange={(e) => handleFilterChange("ativo", e.target.value)}
                className="border-green-200 dark:border-green-800 focus:border-green-500 dark:focus:border-green-400"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Métricas Principais */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600 dark:text-green-400">Total de Ativos</p>
                <p className="text-3xl font-bold text-green-800 dark:text-green-200">
                  {overviewData?.total_ativos || 0}
                </p>
              </div>
              <BarChart3 className="h-8 w-8 text-green-600 dark:text-green-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Valor Total</p>
                <p className="text-3xl font-bold text-blue-800 dark:text-blue-200">
                  R$ {(overviewData?.valor_total || 0).toLocaleString('pt-BR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  })}
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-blue-600 dark:text-blue-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-purple-200 dark:border-purple-800 bg-purple-50 dark:bg-purple-900/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-purple-600 dark:text-purple-400">Indexadores</p>
                <p className="text-3xl font-bold text-purple-800 dark:text-purple-200">
                  {overviewData?.total_indexadores || 0}
                </p>
              </div>
              <PieChart className="h-8 w-8 text-purple-600 dark:text-purple-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-900/20">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-orange-600 dark:text-orange-400">Crescimento</p>
                <p className="text-3xl font-bold text-orange-800 dark:text-orange-200">+12.5%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-orange-600 dark:text-orange-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos e Análises */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Distribuição por Indexador */}
        <Card className="border-green-200 dark:border-green-800">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-800 dark:text-green-300">
              <PieChart className="h-5 w-5" />
              Distribuição por Indexador
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {overviewData?.indexadores?.map((item, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-medium text-foreground">{item.nome}</span>
                    <span className="text-sm text-muted-foreground">
                      {item.quantidade} ativos ({item.percentual}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className={cn(
                        "h-2 rounded-full transition-all duration-500",
                        index === 0 && "bg-green-500 dark:bg-green-400",
                        index === 1 && "bg-blue-500 dark:bg-blue-400",
                        index === 2 && "bg-purple-500 dark:bg-purple-400"
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
        <Card className="border-green-200 dark:border-green-800">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-800 dark:text-green-300">
              <Target className="h-5 w-5" />
              Top Ativos por Valor
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {overviewData?.top_ativos?.map((ativo, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                  <div>
                    <p className="font-medium text-foreground">{ativo.codigo}</p>
                    <p className="text-sm text-muted-foreground">{ativo.indexador}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-green-600 dark:text-green-400">
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
      <Card className="border-green-200 dark:border-green-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-800 dark:text-green-300">
            <Activity className="h-5 w-5" />
            Evolução Mensal
          </CardTitle>
          <CardDescription>
            Quantidade de ativos e valor total por mês
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {evolucaoData?.evolucao?.map((mes, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center">
                    <Calendar className="h-6 w-6 text-green-600 dark:text-green-400" />
                  </div>
                  <div>
                    <p className="font-semibold text-lg text-foreground">{mes.mes}</p>
                    <p className="text-sm text-muted-foreground">{mes.quantidade} ativos</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                    R$ {mes.valor.toLocaleString('pt-BR')}
                  </p>
                  <p className="text-sm text-muted-foreground">Valor total</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
