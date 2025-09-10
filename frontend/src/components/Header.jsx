import { Link, NavLink } from "react-router-dom";
import ThemeToggle from "./ThemeToggle";
import { Button } from "@/components/ui/button";

const linkBase = "px-3 py-2 rounded-xl hover:bg-muted/60";
const active = ({ isActive }) => (isActive ? "bg-muted/60" : "");

export default function Header() {
  return (
    <header className="bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/70 sticky top-0 z-10">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">

        <Link to="/" className="font-semibold tracking-tight">
          fundsys<span className="text-green-600 dark:text-primary">.ui</span>
        </Link>

        <nav className="flex items-center gap-1">
          <NavLink to="/" className={({isActive}) => `${linkBase} ${active({isActive})}`}>Home</NavLink>
          <NavLink to="/insights" className={({isActive}) => `${linkBase} ${active({isActive})}`}>Insights</NavLink>
        </nav>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Button asChild variant="outline" size="sm">
            <Link to="/login">Entrar</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
