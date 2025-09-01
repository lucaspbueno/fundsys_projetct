import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Moon, Sun } from "lucide-react";
import { getStoredTheme, applyTheme } from "@/utils/theme";

export default function ThemeToggle() {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    // Inicializa estado local com o que já está aplicado pelo initTheme()
    const current = getStoredTheme() ?? (document.documentElement.classList.contains("dark") ? "dark" : "light");
    setTheme(current);
  }, []);

  function toggle() {
    const next = theme === "dark" ? "light" : "dark";
    applyTheme(next);   // usa suas utils: seta .dark e salva localStorage
    setTheme(next);
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            variant="outline"
            size="icon"
            onClick={toggle}
            aria-label="Alternar tema"
            className="h-10 w-10 rounded-full"
          >
            <Sun className="h-[1.1rem] w-[1.1rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-[1.1rem] w-[1.1rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">
              {theme === "dark" ? "Modo claro" : "Modo escuro"}
            </span>
          </Button>
        </TooltipTrigger>
        <TooltipContent side="bottom">
          {theme === "dark" ? "Claro" : "Escuro"}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
