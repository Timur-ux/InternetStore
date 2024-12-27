import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { LogInOutProcess } from "../../services/LogInOutProcess";
import style from "../../style";
import {
  AuthStatus,
  selectAuthData,
  selectAuthStatus,
} from "../reducers/authData";

const Profile = () => {
  const [display, setDisplay] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const authStatus = useSelector(selectAuthStatus);
  const authData = useSelector(selectAuthData);

  const items = [
    {
      title: "cart",
      action: () => navigate("/cart"),
    },
    {
      title: authStatus == AuthStatus.logged ? "Log out" : "Log in",
      action: async () => (await LogInOutProcess(authStatus, authData.token))({ dispatch, navigate }),
    },
  ];
  if (authStatus == AuthStatus.logged) {
    items.push({
      title: "Баланс: " + authData.balance,
      action: () => {},
    });
  }

  const itemsElements = items.map((item) => (
    <button style={style.profileButton} onClick={item.action}>
      {item.title}
    </button>
  ));

  return (
    <div style={{ ...style.profileLine }}>
      {display && itemsElements}
      <button
        style={{ ...style.profileButton }}
        onClick={() => setDisplay(!display)}
      >
        {authStatus == AuthStatus.logged ? authData.login : "Profile"}
      </button>
    </div>
  );
};

export default Profile;
