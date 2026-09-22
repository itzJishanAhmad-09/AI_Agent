import { useState } from "react";

export function InputBar({
  onSend,
  disabled,
}: {
  onSend: (text: string) => void;
  disabled: boolean;
}) {
  const [value, setValue] = useState("");

  function submit() {
    if (!value.trim() || disabled) return;
    onSend(value);
    setValue("");
  }

  return (
    <div className="input-bar">
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submit()}
        placeholder="Ask anything..."
        disabled={disabled}
      />
      <button onClick={submit} disabled={disabled || !value.trim()}>
        {disabled ? "..." : "Send"}
      </button>
    </div>
  );
}