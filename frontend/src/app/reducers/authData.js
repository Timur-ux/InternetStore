import { createSlice } from "@reduxjs/toolkit";

export const AuthStatus = {
  logged: "LoggedIn",
  notLogged: "NotLoggedIn",
};

const initialState = {
  data: {
    status: AuthStatus.notLogged,
    login: "",
    password: "",
    balance: 0,
    token: "",
  },
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setToken(state, action) {
      console.log("AuthData: setToken: ", action.payload);
      state.data.token = action.payload;
    },
    setLogin(state, action) {
      state.data.login = action.payload;
    },
    setPassword(state, action) {
      state.data.password = action.payload;
    },
    setBalance(state, action) {
      state.data.balance = action.payload;
    },
    onLogIn(state, action) {
      state.data.status = AuthStatus.logged;
    },
    onLogOut(state, action) {
      state.data.status = AuthStatus.notLogged;
    },
  },
});

export const {
  setLogin,
  setPassword,
  setBalance,
  setToken,
  onLogOut,
  onLogIn,
} = authSlice.actions;
export default authSlice.reducer;

export const selectAuthData = (state) => state.authData.data;
export const selectAuthStatus = (state) => {
  return state.authData.data.status;
};
