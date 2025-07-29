import { useMemo, useState, useEffect } from 'react'
import { Box, FormControl, InputLabel, MenuItem, Select, Stack, Typography } from '@mui/material'
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, BarChart, Bar } from 'recharts'
import { QueryRunResponse } from '../types'

type Props = { result: QueryRunResponse | null }
export default function ChartView({ result }: Props) {
  const [xField, setXField] = useState<string>('')
  const [yField, setYField] = useState<string>('')

  useEffect(() => {
    if (!result || result.columns.length < 2) {
      setXField('')
      setYField('')
      return
    }
    setXField(result.columns[0])
    setYField(result.columns[1])
  }, [result])

  const options = result?.columns || []
  const data = useMemo(() => {
    if (!result) return []
    return result.rows.map(r => {
      const obj: any = {}
      result.columns.forEach((c, i) => (obj[c] = r[i]))
      return obj
    })
  }, [result])

  return (
    <Box>
      <Typography variant="h6" sx={{ mb: 1 }}>График</Typography>
      <Stack direction="row" gap={2} sx={{ mb: 2 }}>
        <FormControl size="small" sx={{ minWidth: 200 }}>
            <InputLabel>X</InputLabel>
            <Select label="X" value={xField} onChange={e => setXField(e.target.value)}>
              {options.map(o => <MenuItem key={o} value={o}>{o}</MenuItem>)}
            </Select>
        </FormControl>
        <FormControl size="small" sx={{ minWidth: 200 }}>
            <InputLabel>Y</InputLabel>
            <Select label="Y" value={yField} onChange={e => setYField(e.target.value)}>
              {options.map(o => <MenuItem key={o} value={o}>{o}</MenuItem>)}
            </Select>
        </FormControl>
      </Stack>
      {data.length > 0 && xField && yField && (
        <Stack gap={4}>
          <LineChart width={960} height={360} data={data} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={xField} />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey={yField} stroke="#1976d2" strokeWidth={2} />
          </LineChart>
          <BarChart width={960} height={360} data={data} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={xField} />
            <YAxis />
            <Tooltip />
            <Bar dataKey={yField} fill="#1976d2" fillOpacity={0.7} />
          </BarChart>
        </Stack>
      )}
    </Box>
  )
}
