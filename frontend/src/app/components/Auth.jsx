import React, { useEffect } from "react";
import { useSelector } from "react-redux";
import style from "../../style";
import { setLogin, setPassword } from "../reducers/authData";
import { store } from "../store";
import TextField from "./TextField";

const Auth = () => {
  var authData = {};
  useEffect(() => {
    const unsubscribe = store.subscribe(() => {
      authData = store.getState().authData.data;
    });
    return () => unsubscribe();
  }, []);

  const onAuthClick = () => {
    const { login, password } = authData;
    console.log("auth processing:", authData);
  };

  return (
    <div style={{ ...style.infoBlock, ...style.centered }}>
      <p>Login</p>
      <TextField onBlur={setLogin} />
      <p>Password</p>
      <TextField onBlur={setPassword} type="password" />
      <br />
      <button style={style.centered} onClick={onAuthClick}>
        Submit
      </button>
    </div>
  );
};

export default Auth;
