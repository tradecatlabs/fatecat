// SSR: redirect to register page
export async function getServerSideProps() {
  return {
    redirect: {
      destination: '/register',
      permanent: false, // 使用临时重定向
    },
  };
}

// 这个组件实际上不会被渲染，因为会直接重定向
export default function Home() {
  return null;
}
