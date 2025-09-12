import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { env } from "@/config/env";

const API_BASE = "/api/enrichment";

export function useEnrichmentStatus() {
  return useQuery({
    queryKey: ["enrichment", "status"],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/status`);
      return data;
    },
    staleTime: 30 * 1000, // 30 segundos
  });
}

export function useEnrichAtivo() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (ativoId) => {
      const { data } = await axios.post(`${API_BASE}/enrich/${ativoId}`);
      return data;
    },
    onSuccess: () => {
      // Invalidar queries relacionadas
      queryClient.invalidateQueries({ queryKey: ["analytics"] });
      queryClient.invalidateQueries({ queryKey: ["enrichment"] });
    },
  });
}

export function useEnrichMultipleAtivos() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ ativoIds, background = false }) => {
      const { data } = await axios.post(`${API_BASE}/enrich/bulk`, {
        ativo_ids: ativoIds,
        background
      });
      return data;
    },
    onSuccess: () => {
      // Invalidar queries relacionadas
      queryClient.invalidateQueries({ queryKey: ["analytics"] });
      queryClient.invalidateQueries({ queryKey: ["enrichment"] });
    },
  });
}

export function useEnrichPendingAtivos() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ limit = 50, background = false }) => {
      const params = new URLSearchParams();
      if (limit) params.append("limit", limit);
      if (background) params.append("background", "true");
      
      const { data } = await axios.post(`${API_BASE}/enrich/pending?${params}`);
      return data;
    },
    onSuccess: () => {
      // Invalidar queries relacionadas
      queryClient.invalidateQueries({ queryKey: ["analytics"] });
      queryClient.invalidateQueries({ queryKey: ["enrichment"] });
    },
  });
}

export function useAtivoEnrichedData(ativoId) {
  return useQuery({
    queryKey: ["enrichment", "ativo", ativoId],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/ativos/${ativoId}/enriched`);
      return data;
    },
    enabled: !!ativoId,
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
}

