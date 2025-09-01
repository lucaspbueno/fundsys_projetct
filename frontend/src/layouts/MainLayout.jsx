import Header from "../components/Header";
import Sidebar from "../components/Sidebar";

export default function MainLayout({ children }) {
  return (
    <div className="min-h-dvh bg-bg text-text">
      <Sidebar />
      {/* Empurra tudo para a direita no desktop */}
      <div className="md:pl-[260px]">
        <Header />
        <main className="py-6">
          <div className="max-w-7xl mx-auto px-4">{children}</div>
        </main>
      </div>
    </div>
  );
}
