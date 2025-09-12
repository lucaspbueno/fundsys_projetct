import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { env } from "@/config/env";

const API_BASE = "/api/fundo";

export function useFundos(limit = 50, offset = 0) {
  return useQuery({
    queryKey: ["fundos", limit, offset],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/?limit=${limit}&offset=${offset}`);
      return data;
    },
    staleTime: 2 * 60 * 1000, // 2 minutos
  });
}

export function useFundoDetalhes(fundoId) {
  return useQuery({
    queryKey: ["fundo", fundoId],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/${fundoId}`);
      return data;
    },
    enabled: !!fundoId,
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
}

export function useUploadFundo() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (arquivo) => {
      const formData = new FormData();
      formData.append('arquivo', arquivo);
      
      const { data } = await axios.post(`${API_BASE}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return data;
    },
    onSuccess: () => {
      // Invalidar queries relacionadas
      queryClient.invalidateQueries({ queryKey: ["fundos"] });
      queryClient.invalidateQueries({ queryKey: ["analytics"] });
    },
  });
}

export function useDeleteFundo() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (fundoId) => {
      const { data } = await axios.delete(`${API_BASE}/${fundoId}`);
      return data;
    },
    onSuccess: () => {
      // Invalidar queries relacionadas
      queryClient.invalidateQueries({ queryKey: ["fundos"] });
      queryClient.invalidateQueries({ queryKey: ["analytics"] });
    },
  });
}
