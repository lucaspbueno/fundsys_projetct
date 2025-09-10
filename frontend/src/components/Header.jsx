import { Link, NavLink } from "react-router-dom";
import ThemeToggle from "./ThemeToggle";
import { Button } from "@/components/ui/button";

export default function Header() {
  return (
    <header className="bg-background/95 backdrop-blur-md border-b border-border/50 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="font-bold text-xl tracking-tight group">
          fundsys<span className="text-primary group-hover:text-primary/80 transition-colors">.ui</span>
        </Link>

        <nav className="flex items-center gap-2">
          <NavLink 
            to="/" 
            className={({isActive}) => `px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
              isActive 
                ? 'bg-primary/10 text-primary border border-primary/20' 
                : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
            }`}
          >
            Home
          </NavLink>
          <NavLink 
            to="/insights" 
            className={({isActive}) => `px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
              isActive 
                ? 'bg-primary/10 text-primary border border-primary/20' 
                : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
            }`}
          >
            Insights
          </NavLink>
        </nav>

        <div className="flex items-center gap-3">
          <ThemeToggle />
          <Button asChild variant="outline" size="sm" className="border-primary/20 text-primary hover:bg-primary/10 hover:border-primary/30">
            <Link to="/login">Entrar</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
