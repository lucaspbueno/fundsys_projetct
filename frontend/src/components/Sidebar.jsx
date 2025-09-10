// src/components/Sidebar.jsx
import { NavLink } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Upload, History, BarChart3, HelpCircle } from "lucide-react";
import { cn } from "@/lib/utils";

const LINKS = [
  { to: "/", label: "Importar XML", icon: Upload, end: true },
  { to: "/history", label: "Histórico", icon: History },
  { to: "/insights", label: "Insights", icon: BarChart3 },
  { to: "/ajuda", label: "Ajuda", icon: HelpCircle },
];

function NavItem({ to, label, icon: Icon, end }) {
  return (
    <NavLink to={to} end={end} className="block">
      {({ isActive }) => (
        <Button
          type="button"
          variant="ghost"
          className={cn(
            // layout
            "w-full justify-start gap-2 rounded-xl px-3",
            // cores padrão + HOVER visível nos 2 temas
            "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
            // FOCO acessível
            "focus-visible:ring-2 focus-visible:ring-sidebar-ring focus-visible:outline-none",
            // ESTADO ATIVO (rota selecionada) — com transição suave
            isActive &&
              "bg-sidebar-accent text-sidebar-accent-foreground",
            // SUAVIZA transições de cor/tema
            "transition-colors duration-300 ease-in-out"
          )}
          aria-current={isActive ? "page" : undefined}
        >
          <Icon className="h-4 w-4 shrink-0" />
          <span className="truncate">{label}</span>
        </Button>
      )}
    </NavLink>
  );
}

export default function Sidebar() {
  return (
    <aside
      aria-label="Barra lateral"
      className={cn(
        "hidden md:flex fixed inset-y-0 left-0 w-[260px]",
        "bg-sidebar text-sidebar-foreground border-r border-sidebar-border",
        // SUAVIZA o fundo/borda/texto da própria sidebar na troca de tema
        "transition-colors duration-300 ease-in-out"
      )}
    >
      <ScrollArea className="h-full w-full">
        <div className="p-4 space-y-4">
          <div className="px-1">
            <p className="text-xs font-medium text-muted-foreground tracking-wide transition-colors duration-300">
              Navegação
            </p>
          </div>

          <nav className="flex flex-col gap-2">
            {LINKS.map((link) => (
              <NavItem key={link.to} {...link} />
            ))}
          </nav>
        </div>
      </ScrollArea>
    </aside>
  );
}
