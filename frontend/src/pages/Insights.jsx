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
          <RefreshCw className="h-6 w-6 animate-spin text-green-600" />
          <span className="text-lg">Carregando insights...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Insights do Fundo</h1>
          <p className="text-gray-600 mt-1">
            Análises e métricas dos dados de investimento
          </p>
        </div>
        <div className="flex gap-3">
          <Button
            onClick={handleRefresh}
            variant="outline"
            className="border-green-200 text-green-700 hover:bg-green-50"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Atualizar
          </Button>
          <Button
            onClick={handleExport}
            className="bg-green-600 hover:bg-green-700 text-white"
          >
            <Download className="h-4 w-4 mr-2" />
            Exportar
          </Button>
        </div>
      </div>

      {/* Filtros */}
      <Card className="border-green-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-800">
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
                className="border-green-200 focus:border-green-500"
              />
            </div>
            <div>
              <Label htmlFor="dateTo">Data Final</Label>
              <Input
                id="dateTo"
                type="date"
                value={filters.dateTo}
                onChange={(e) => handleFilterChange("dateTo", e.target.value)}
                className="border-green-200 focus:border-green-500"
              />
            </div>
            <div>
              <Label htmlFor="indexador">Indexador</Label>
              <Input
                id="indexador"
                placeholder="Ex: DI1, IAP, PRE"
                value={filters.indexador}
                onChange={(e) => handleFilterChange("indexador", e.target.value)}
                className="border-green-200 focus:border-green-500"
              />
            </div>
            <div>
              <Label htmlFor="ativo">Código do Ativo</Label>
              <Input
                id="ativo"
                placeholder="Ex: CRA02300FFL"
                value={filters.ativo}
                onChange={(e) => handleFilterChange("ativo", e.target.value)}
                className="border-green-200 focus:border-green-500"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Métricas Principais */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="border-green-200 bg-green-50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600">Total de Ativos</p>
                <p className="text-3xl font-bold text-green-800">
                  {overviewData?.total_ativos || 0}
                </p>
              </div>
              <BarChart3 className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-blue-200 bg-blue-50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-600">Valor Total</p>
                <p className="text-3xl font-bold text-blue-800">
                  R$ {(overviewData?.valor_total || 0).toLocaleString('pt-BR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  })}
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-purple-200 bg-purple-50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-purple-600">Indexadores</p>
                <p className="text-3xl font-bold text-purple-800">
                  {overviewData?.total_indexadores || 0}
                </p>
              </div>
              <PieChart className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>

        <Card className="border-orange-200 bg-orange-50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-orange-600">Crescimento</p>
                <p className="text-3xl font-bold text-orange-800">+12.5%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos e Análises */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Distribuição por Indexador */}
        <Card className="border-green-200">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-800">
              <PieChart className="h-5 w-5" />
              Distribuição por Indexador
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {overviewData?.indexadores?.map((item, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">{item.nome}</span>
                    <span className="text-sm text-gray-600">
                      {item.quantidade} ativos ({item.percentual}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={cn(
                        "h-2 rounded-full transition-all duration-500",
                        index === 0 && "bg-green-500",
                        index === 1 && "bg-blue-500",
                        index === 2 && "bg-purple-500"
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
        <Card className="border-green-200">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-800">
              <Target className="h-5 w-5" />
              Top Ativos por Valor
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {overviewData?.top_ativos?.map((ativo, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium">{ativo.codigo}</p>
                    <p className="text-sm text-gray-600">{ativo.indexador}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-green-600">
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
      <Card className="border-green-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-800">
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
              <div key={index} className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                    <Calendar className="h-6 w-6 text-green-600" />
                  </div>
                  <div>
                    <p className="font-semibold text-lg">{mes.mes}</p>
                    <p className="text-sm text-gray-600">{mes.quantidade} ativos</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-green-600">
                    R$ {mes.valor.toLocaleString('pt-BR')}
                  </p>
                  <p className="text-sm text-gray-600">Valor total</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
