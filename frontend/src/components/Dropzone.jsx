import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { FileUp } from "lucide-react";
import { cn } from "@/lib/utils";

export default function Dropzone({ onFiles }) {
  const inputRef = useRef(null);
  const [dragOver, setDragOver] = useState(false);

  function handleBrowse() {
    inputRef.current?.click();
  }

  function toArrayLike(files) {
    return files ? Array.from(files) : [];
  }

  function handleSelected(e) {
    const list = toArrayLike(e.target.files);
    if (!list.length) return;
    onFiles?.(list);
    // permite selecionar o mesmo arquivo novamente
    e.target.value = "";
  }

  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
    const list = toArrayLike(e.dataTransfer?.files);
    if (!list.length) return;
    onFiles?.(list);
  }

  function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(true);
  }

  function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
  }

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={handleBrowse}
      onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && handleBrowse()}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      className={cn(
        "flex flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed",
        "px-6 py-10 text-center",
        "bg-muted/40 border-border/70 hover:bg-muted/60",
        "transition-colors",
        dragOver && "bg-muted/70 border-ring"
      )}
      aria-label="Área para soltar arquivos ou clicar para selecionar"
    >
      <FileUp className="h-8 w-8 text-muted-foreground" aria-hidden="true" />
      <div className="space-y-1">
        <p className="text-sm">
          <span className="font-medium">Solte os arquivos XML</span> aqui
        </p>
        <p className="text-xs text-muted-foreground">ou</p>
      </div>
      <Button type="button" variant="outline" className="rounded-xl">
        Selecionar arquivos
      </Button>

      <input
        ref={inputRef}
        type="file"
        accept=".xml"
        multiple
        onChange={handleSelected}
        className="hidden"
        aria-hidden="true"
      />
    </div>
  );
}
