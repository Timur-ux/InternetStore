import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { processAuth } from "../../services/auth";
import style from "../../style";
import { onLogIn, selectAuthData, setLogin, setPassword } from "../reducers/authData";
import { store } from "../store";
import TextField from "./TextField";

const Auth = () => {
  var authData = useSelector(selectAuthData);
  const [message, setMessage] = useState("");
  const [color, setColor] = useState("green");
  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    const unsubscribe = store.subscribe(() => {
      authData = store.getState().authData.data;
    });
    return () => unsubscribe();
  }, []);

  const onAuthClick = async () => {
    const { login, password } = authData;
    const response = await processAuth({ login, password })
      .then(() => {
        setMessage(
          "Успешный вход в магазин",
        );
        dispatch(onLogIn());
        setColor("green");
        navigate("/");
      })
      .catch(() => {
        setMessage("Ошибка: неправильный логин или пароль");
        setColor("red");
      });
  };

  return (
    <div style={{ ...style.infoBlock, ...style.centered }}>
      <div>
        <p style={{ color: color }}>{message}</p>
      </div>
      <p>Login</p>
      <TextField onBlur={setLogin} />
      <p>Password</p>
      <TextField onBlur={setPassword} type="password" />
      <br />
      <div style={style.itemsLine}>
        <button style={style.centered} onClick={onAuthClick}>
          Submit
        </button>
        <a href="/register">Регистрация</a>
      </div>
    </div>
  );
};

export default Auth;
