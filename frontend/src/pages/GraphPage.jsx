import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useProject } from "../context/ProjectContext";
import { useLiveGraph } from "../hooks/useLiveGraph";
import GraphCanvas from "../components/GraphCanvas";


export default function GraphPage() {
  const { projectId } = useParams();
  const { current, setCurrent } = useProject();
  const [filters, setFilters] = useState({ updatedOnly: false, imports: true, calls: true });
  const { graph, connected } = useLiveGraph(projectId);

  useEffect(() => { 
    if (projectId && current !== projectId) setCurrent(projectId); 
  }, [projectId, current, setCurrent]);

  return (
    <div className="flex-1 p-4">
      <div className="flex items-center gap-3 mb-3">
        <h2 className="text-slate-200 text-xl font-medium">
          Graph <span className="ml-2 text-xs bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded">LIVE</span>
        </h2>
        <span className={`text-xs px-2 py-0.5 rounded ${connected ? 'bg-emerald-600/20 text-emerald-300' : 'bg-slate-700/30 text-slate-400'}`}>
          {connected ? 'Connected' : 'Offline'}
        </span>
        <div className="ml-auto flex items-center gap-4 text-sm text-slate-300">
          <label className="inline-flex items-center gap-2">
            <input 
              type="checkbox" 
              className="accent-orange-400" 
              checked={filters.updatedOnly} 
              onChange={(e) => setFilters({ ...filters, updatedOnly: e.target.checked })} 
            />
            Updated only
          </label>
          <label className="inline-flex items-center gap-2">
            <input 
              type="checkbox" 
              className="accent-sky-400" 
              checked={filters.imports} 
              onChange={(e) => setFilters({ ...filters, imports: e.target.checked })} 
            />
            Imports
          </label>
          <label className="inline-flex items-center gap-2">
            <input 
              type="checkbox" 
              className="accent-emerald-400" 
              checked={filters.calls} 
              onChange={(e) => setFilters({ ...filters, calls: e.target.checked })} 
            />
            Calls
          </label>
        </div>
      </div>
      <div className="bg-[#0e1627] border border-slate-800 rounded-xl p-2">
        <GraphCanvas graph={graph} filters={filters} />
      </div>
    </div>
  );
}