import React, { useEffect, useMemo, useState } from "react";
import "./App.scss";
import { ItemList } from "./components/ItemList";
import { Listing } from "./components/Listing";

function App() {
  const [open, setOpen] = useState<boolean>(false);
  const [add, setAdd] = useState<boolean>(false);
  const handleAdd = (e: boolean) => setAdd(e);
  const updateOpen = () => setOpen(!open);
  return (
    <div>
      <header>
        <p className="Title">
          <b>Mercari build shop</b>
        </p>
        <div className="btn-box">
          <button onClick={() => setOpen(!open)} className="btn">
            <b>Add Item</b>
          </button>
        </div>
      </header>
      <div>
        <Listing open={open} updateOpen={updateOpen} handleAdd={handleAdd} />
      </div>
      <div>
        <ItemList add={add} handleAdd={handleAdd} />
      </div>
    </div>
  );
}

export default App;
