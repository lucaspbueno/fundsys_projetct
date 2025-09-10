import { useMutation } from "@tanstack/react-query";
import { env } from "@/config/env";
import axios from "axios";

export function useUploadXml() {
  return useMutation({
    mutationFn: async (files) => {
      const fd = new FormData();
      files.forEach((f) => fd.append("ls_files", f));
      
      const { data } = await axios.post(env.uploadUrl, fd, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return data;
    },
  });
}
