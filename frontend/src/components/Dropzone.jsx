import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { FileUp } from "lucide-react";
import { cn } from "@/lib/utils";

export default function Dropzone({ onFiles, disabled = false }) {
  const inputRef = useRef(null);
  const [dragOver, setDragOver] = useState(false);

  function handleBrowse() {
    if (disabled) return;
    inputRef.current?.click();
  }

  function toArrayLike(files) {
    return files ? Array.from(files) : [];
  }

  function handleSelected(e) {
    if (disabled) return;
    const list = toArrayLike(e.target.files);
    if (!list.length) return;
    onFiles?.(list);
    // permite selecionar o mesmo arquivo novamente
    e.target.value = "";
  }

  function handleDrop(e) {
    if (disabled) return;
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
    const list = toArrayLike(e.dataTransfer?.files);
    if (!list.length) return;
    onFiles?.(list);
  }

  function handleDragOver(e) {
    if (disabled) return;
    e.preventDefault();
    e.stopPropagation();
    setDragOver(true);
  }

  function handleDragLeave(e) {
    if (disabled) return;
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
        "flex flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed",
        "px-8 py-12 text-center",
        "bg-muted/30 border-primary/20 hover:bg-muted/50 hover:border-primary/30",
        "transition-all duration-300 ease-in-out",
        dragOver && !disabled && "bg-primary/5 border-primary/40 scale-[1.02]",
        disabled && "opacity-50 cursor-not-allowed bg-muted/20"
      )}
      aria-label="Área para soltar arquivos ou clicar para selecionar"
    >
      <FileUp className="h-10 w-10 text-primary/60" aria-hidden="true" />
      <div className="space-y-2">
        <p className="text-base font-medium text-foreground">
          {disabled ? "Processando arquivo..." : "Solte os arquivos XML aqui"}
        </p>
        {!disabled && (
          <p className="text-sm text-muted-foreground">
            ou clique para selecionar
          </p>
        )}
      </div>
      <Button 
        type="button" 
        variant="outline" 
        className="rounded-lg border-primary/20 text-primary hover:bg-primary/10 hover:border-primary/30"
        disabled={disabled}
      >
        {disabled ? "Processando..." : "Selecionar arquivos"}
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
