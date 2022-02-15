//import '../styles/globals.css'
import 'antd/dist/antd.css';

import { Layout, PageHeader } from 'antd';
const { Header, Content, Footer } = Layout;

import { Typography } from 'antd';

const { Title } = Typography;

function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <Header style={{ textAlign: 'center' }}>
        <div>
        <Title type="secondary" style={{ color: 'white' }}>ABIGAIL</Title>
        </div>
      </Header>
      <Component {...pageProps} />
    </Layout>
  )
  
}

export default MyApp
