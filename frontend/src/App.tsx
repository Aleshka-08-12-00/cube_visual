import { CssBaseline, Container } from '@mui/material'
import Explorer from './pages/Explorer'

export default function App() {
  return (
    <>
      <CssBaseline />
      <Container maxWidth="xl" sx={{ py: 2 }}>
        <Explorer />
      </Container>
    </>
  )
}
