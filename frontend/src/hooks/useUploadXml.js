import { useMutation } from "@tanstack/react-query";
import axios from "axios";

export function useUploadXml() {
  return useMutation({
    mutationFn: async (files) => {
      const fd = new FormData();
      files.forEach((f) => fd.append("files", f));
      // ajuste a URL conforme seu backend (FastAPI)
      const { data } = await axios.post("/api/upload", fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return data;
    },
  });
}
