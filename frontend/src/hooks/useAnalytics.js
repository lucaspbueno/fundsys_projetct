import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { env } from "@/config/env";

const API_BASE = "/api/analytics";

export function useOverview(enriched = false, fundoId = null) {
  return useQuery({
    queryKey: ["analytics", "overview", enriched, fundoId],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (enriched) params.append("enriched", "true");
      if (fundoId) params.append("fundo_id", fundoId);
      
      const { data } = await axios.get(`${API_BASE}/overview?${params}`);
      return data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
}

export function useAtivos(filters = {}) {
  return useQuery({
    queryKey: ["analytics", "ativos", filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.fundoId) params.append("fundo_id", filters.fundoId);
      if (filters.indexador) params.append("indexador", filters.indexador);
      if (filters.limit) params.append("limit", filters.limit);
      if (filters.offset) params.append("offset", filters.offset);
      if (filters.enriched) params.append("enriched", "true");
      
      const { data } = await axios.get(`${API_BASE}/ativos?${params}`);
      return data;
    },
    staleTime: 2 * 60 * 1000, // 2 minutos
  });
}

export function useIndexadores() {
  return useQuery({
    queryKey: ["analytics", "indexadores"],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/indexadores`);
      return data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
}

export function useEvolucaoMensal(ano = null) {
  return useQuery({
    queryKey: ["analytics", "evolucao-mensal", ano],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (ano) params.append("ano", ano);
      
      const { data } = await axios.get(`${API_BASE}/evolucao-mensal?${params}`);
      return data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
}
