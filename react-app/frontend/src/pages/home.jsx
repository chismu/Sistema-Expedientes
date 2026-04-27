import { useEffect, useState } from "react";
import API from "../services/api";

function Home() {
  const [expedientes, setExpedientes] = useState([]);

  useEffect(() => {
    API.get("/expedientes")
      .then((res) => setExpedientes(res.data))
      .catch((err) => console.error(err));
  }, []);

  const getColor = (color) => {
    if (color === "rojo") return "danger";
    if (color === "amarillo") return "warning";
    return "success";
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Expedientes</h2>

      <div className="row">
        {expedientes.map((exp) => (
          <div className="col-md-4 mb-3" key={exp.id}>
            <div className={`card border-${getColor(exp.color)}`}>
              <div className={`card-header bg-${getColor(exp.color)} text-white`}>
                {exp.numero}
              </div>

              <div className="card-body">
                <p><strong>Carátula:</strong> {exp.caratula}</p>
                <p><strong>Fecha:</strong> {exp.fecha_ingreso}</p>

                <button className="btn btn-primary btn-sm me-2">
                  Ver
                </button>

                <button className="btn btn-danger btn-sm">
                  Finalizar
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;