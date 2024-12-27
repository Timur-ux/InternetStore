import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { processRegister } from "../../services/register";
import style from "../../style";
import { selectAuthData, setLogin, setPassword } from "../reducers/authData";
import { store } from "../store";
import TextField from "./TextField";

const Register = () => {
  var authData = useSelector(selectAuthData);
  const [message, setMessage] = useState("");
  const [color, setColor] = useState("green");

  useEffect(() => {
    const unsubscribe = store.subscribe(() => {
      authData = store.getState().authData.data;
    });
    return () => unsubscribe();
  }, []);

  const onRegisterClick = async () => {
    const { login, password } = authData;
    const response = await processRegister({ login, password })
      .then(() => {
        setMessage(
          "Регистрация прошла успешно, теперь вы можете пройти в свой профиль",
        );
        setColor("green");
      })
      .catch(() => {
        setMessage("Ошибка, пользователь с таким именем уже существует");
        setColor("red");
      });
  };

  return (
    <div style={{ ...style.infoBlock, ...style.centered }}>
      <div>
        <p style={{ color: color }}>{message}</p>
      </div>
      <p>Login</p>
      <TextField onChange={setLogin} />
      <p>Password</p>
      <TextField onChange={setPassword} type="password" />
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
