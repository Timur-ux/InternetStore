import React, { useEffect } from "react";
import style from "../../style";
import { setLogin, setPassword } from "../reducers/authData";
import { store } from "../store";
import TextField from "./TextField";

const Register = () => {
  var authData = {};
  useEffect(() => {
    const unsubscribe = store.subscribe(() => {
      authData = store.getState().authData.data;
    });
    return () => unsubscribe();
  }, []);

  const onRegisterClick = () => {
    const { login, password } = authData;
    console.log("Register processing:", authData);
  };

  return (
    <div style={{ ...style.infoBlock, ...style.centered }}>
      <p>Login</p>
      <TextField onBlur={setLogin} />
      <p>Password</p>
      <TextField onBlur={setPassword} type="password" />
      <br />
      <div style={style.itemsLine}>
        <button style={style.centered} onClick={onRegisterClick}>
          Submit
        </button>
        <a href="/auth">Авторизация</a>
      </div>
    </div>
  );
};

export default Register;

