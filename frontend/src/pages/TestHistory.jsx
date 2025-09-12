import { useFundos } from "@/hooks/useFundo";

export default function TestHistory() {
  const { data: fundosData, isLoading, error } = useFundos(10, 0);

  console.log("Fundos data:", fundosData);
  console.log("Is loading:", isLoading);
  console.log("Error:", error);

  if (isLoading) {
    return <div>Carregando...</div>;
  }

  if (error) {
    return <div>Erro: {error.message}</div>;
  }

  return (
    <div>
      <h1>Teste de Fundos</h1>
      <p>Total: {fundosData?.total || 0}</p>
      <ul>
        {fundosData?.fundos?.map(fundo => (
          <li key={fundo.id_fundo_investimento}>
            {fundo.nm_fundo_investimento}
          </li>
        ))}
      </ul>
    </div>
  );
}

