import React from "react";
import style from "../../style";

const Footer = (props) => {
  return (
    <div style={{ ...style.footer, ...style.baseBackground }}>
      <div style={style.footerItem}>
        Электронная почта: Боевая@Пчела@Не@Пользуется@Почтой@bees.radio <br />
      </div>
      <div style={style.footerItem}>
        Адрес: Пасека, пчелиный общепит, 7 сота
      </div>
    </div>
  );
};

export default Footer;
