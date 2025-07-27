import { DataGrid, GridColDef } from '@mui/x-data-grid'
import { useMemo } from 'react'
import { Box, Typography } from '@mui/material'
import { QueryRunResponse } from '../types'

type Props = { result: QueryRunResponse | null }
export default function ResultsTable({ result }: Props) {
  const cols = useMemo<GridColDef[]>(() => {
    if (!result) return []
    return result.columns.map((c, i) => ({ field: String(i), headerName: c, flex: 1, minWidth: 120, sortable: true }))
  }, [result])
  const rows = useMemo(() => {
    if (!result) return []
    return result.rows.map((r, idx) => {
      const obj: any = { id: idx }
      r.forEach((v: any, i: number) => (obj[String(i)] = v))
      return obj
    })
  }, [result])
  return (
    <Box>
      <Typography variant="h6" sx={{ mb: 1 }}>Результат</Typography>
      <div style={{ height: 520, width: '100%' }}>
        <DataGrid rows={rows} columns={cols} density="compact" />
      </div>
    </Box>
  )
}
