import { createSlice } from "@reduxjs/toolkit";

export const AuthStatus = {
  logged: "LoggedIn",
  notLogged: "NotLoggedIn"
};

const initialState = {
  data: {
    status: AuthStatus.notLogged,
    login: "",
    password: "",
  },
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setLogin(state, action) {
      state.data.login = action.payload;
    },
    setPassword(state, action) {
      console.log("Set password: ", action.payload);
      state.data.password = action.payload;
    },
    onLogIn(state, action) {
      state.data.status = AuthStatus.logged;
    },
    onLogOut(state, action) {
      state.data.status = AuthStatus.notLogged;
    },
  },
});

export const { setLogin, setPassword, onLogOut, onLogIn} = authSlice.actions;
export default authSlice.reducer;

export const selectAuthData = (state) => state.authData.data;
export const selectAuthStatus = (state) => {
  return state.authData.data.status
};
