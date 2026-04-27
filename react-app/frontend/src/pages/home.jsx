import { useEffect, useState } from "react";
import { getExpedientes } from "../api/api";
// import ExpedientesTable from "../components/ExpedientesTable";

export default function Home() {
  console.log("Home render");

  return (
    <div className="container">
      <h1>Home cargando</h1>
    </div>
  );
}