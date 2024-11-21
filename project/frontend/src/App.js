import React from "react";
import DealForm from "./components/DealForm";
import CSVUpload from "./components/CSVUpload";
import AdvancedOptions from "./components/AdvancedOptions";

const App = () => {
  return (
    <div>
      <h1>Deal Evaluation App</h1>
      <DealForm />
      <CSVUpload />
      <AdvancedOptions />
    </div>
  );
};

export default App;
