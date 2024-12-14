import React from "react";
import { useDispatch } from "react-redux";
import style from "../../style";

const TextField = ({ onChange = null, onBlur = null, type = "text" }) => {
  const dispatch = useDispatch();
  const onChange_ =
    onChange !== null ? (e) => dispatch(onChange(e.target.value)) : () => {};
  const onBlur_ =
    onBlur !== null ? (e) => dispatch(onBlur(e.target.value)) : () => {};

  return (
    <input
      type={type}
      onChange={onChange_}
      onBlur={onBlur_}
      style={{ ...style.textField, ...style.centered }}
    />
  );
};

export default TextField;
