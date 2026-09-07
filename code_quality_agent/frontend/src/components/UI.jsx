import React from "react";

export const Button = ({ children, onClick, disabled, style: styleProp }) => {
  const defaultStyle = {
    padding: "0.75rem 1.5rem",
    border: "none",
    borderRadius: "4px",
    backgroundColor: "#3498db",
    color: "white",
    fontSize: "1rem",
    cursor: disabled ? "not-allowed" : "pointer",
    transition: "background-color 0.2s",
    ...styleProp,
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{ ...defaultStyle, backgroundColor: disabled ? "#7f8c8d" : "#3498db" }}
    >
      {children}
    </button>
  );
};

export const Card = ({ children, style: styleProp }) => {
  const defaultStyle = {
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    padding: "1.5rem",
    marginBottom: "1.5rem",
    backgroundColor: "white",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.05)",
    ...styleProp,
  };

  return <div style={{ ...defaultStyle, ...styleProp }}>{children}</div>;
};

export const CardHeader = ({ children, style: styleProp }) => {
  return (
    <div
      style={{
        borderBottom: "1px solid #e0e0e0",
        paddingBottom: "0.75rem",
        marginBottom: "0.75rem",
      }}
    >
      {children}
    </div>
  );
};

export const CardTitle = ({ children }) => {
  <h3 style={{ margin: 0, fontSize: "1.25rem" }}>{children}</h3>;
};