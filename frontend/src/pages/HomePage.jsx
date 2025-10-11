import React from "react";
import { Link } from "react-router-dom";
import { useProject } from "../context/ProjectContext";


export default function HomePage() {
  const { current } = useProject();
  return (
    <div className="flex-1 p-6 text-slate-300">
      <h1 className="text-2xl text-slate-100 mb-2">Welcome</h1>
      <p className="mb-4">Choose a project to view its live graph.</p>
      {current && (
        <Link className="inline-block bg-indigo-600/80 hover:bg-indigo-600 text-white px-4 py-2 rounded-md" to={`/projects/${current}/graph`}>
          Go to {current} graph
        </Link>
      )}
    </div>
  );
}