import ExpedientesTable from "../components/ExpedientesTable";
import ExpedienteForm from "../components/ExpedienteForm";
import Estadisticas from "../components/Estadisticas";

export default function Home() {
  return (
    <div className="container mt-4">
      <h2 className="mb-4">Sistema de Expedientes</h2>

      <ExpedienteForm onCreated={() => window.location.reload()} />

      <Estadisticas />
      <ExpedientesTable />
    </div>
  );
}