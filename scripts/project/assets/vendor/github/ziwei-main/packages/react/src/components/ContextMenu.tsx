import type React from "react";

import { createPortal } from "react-dom";

// 类型定义
export interface ContextMenuProps {
  x: number;
  y: number;
  onClose: () => void;
  menuItems: Array<{ label: string; onClick: () => void }>;
}

// 蒙层组件
const Overlay: React.FC<{ onClick: () => void }> = ({ onClick }) => (
  <div
    onClick={onClick}
    style={{
      position: "fixed",
      top: 0,
      left: 0,
      width: "100vw",
      height: "100vh",
      background: "transparent", // 透明背景
      zIndex: 999, // 确保在菜单下方
    }}
  />
);

// 菜单组件
const Menu: React.FC<{
  x: number;
  y: number;
  menuItems: Array<{ label: string; onClick: () => void }>;
  onClose: () => void;
}> = ({ x, y, menuItems, onClose }) => {
  return (
    <div
      style={{
        position: "fixed",
        top: y,
        left: x,
        zIndex: 1000, // 确保在蒙层上方
        width: "200px",
        background: "white",
        borderRadius: "4px",
        boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.12)",
        padding: "8px 0",
      }}
    >
      {menuItems.map((item, index) => (
        <div
          key={item.label}
          onClick={() => {
            item.onClick();
            onClose(); // 点击菜单项后关闭菜单
          }}
          style={{
            padding: "10px 15px",
            fontSize: "14px",
            color: "#212121",
            cursor: "pointer",
            borderBottom: index < menuItems.length - 1 ? "1px solid #e0e0e0" : "none",
          }}
        >
          {item.label}
        </div>
      ))}
    </div>
  );
};

// 主组件
const ContextMenu: React.FC<ContextMenuProps> = ({ x, y, onClose, menuItems }) => {
  return createPortal(
    <>
      <Overlay onClick={onClose} />
      <Menu x={x} y={y} menuItems={menuItems} onClose={onClose} />
    </>,
    document.body,
  );
};

export default ContextMenu;
