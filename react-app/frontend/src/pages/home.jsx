import { useEffect, useState } from "react";
import { getExpedientes } from "../api/api";
import ExpedientesTable from "../components/ExpedientesTable";
import ExpedienteForm from "../components/ExpedienteForm";

export default function Home() {
    const tableRef = useRef();
   return (
        <div className="container mt-4">
            <h2 className="mb-4">Sistema de Expedientes</h2>

            <ExpedienteForm onCreated={() => window.location.reload()} />

            <ExpedientesTable ref={tableRef} />
        </div>
    );
}
