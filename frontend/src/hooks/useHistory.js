import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const API_BASE = "/api/history";

export function useFileHistory(limit = 10, offset = 0) {
  return useQuery({
    queryKey: ["history", "files", { limit, offset }],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/files`, {
        params: { limit, offset }
      });
      return data;
    },
    staleTime: 2 * 60 * 1000, // 2 minutos
  });
}

export function useFileDetails(loteId) {
  return useQuery({
    queryKey: ["history", "file-details", loteId],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/files/${loteId}`);
      return data;
    },
    enabled: !!loteId,
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
}

export function useFileAnalytics(loteId) {
  return useQuery({
    queryKey: ["history", "file-analytics", loteId],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/files/${loteId}/analytics`);
      return data;
    },
    enabled: !!loteId,
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
}
