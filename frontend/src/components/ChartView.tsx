import { useMemo, useState, useEffect } from 'react'
import { Box, FormControl, InputLabel, MenuItem, Select, Stack, Typography } from '@mui/material'
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, BarChart, Bar } from 'recharts'
import { QueryRunResponse } from '../types'

function extractMeasure(mdx: string): string {
  const match = mdx.match(/\[Measures\]\.\[([^\]]+)\]/)
  return match ? match[1] : 'value'
}

function toNumber(v: any): number {
  if (typeof v === 'number') return v
  const n = Number(String(v).replace(',', '.'))
  return isNaN(n) ? 0 : n
}

type Props = { result: QueryRunResponse | null }
export default function ChartView({ result }: Props) {
  const [xField, setXField] = useState<string>('')
  const [yField, setYField] = useState<string>('')
  const [mode, setMode] = useState<'row' | 'column'>('row')

  useEffect(() => {
    if (!result || result.columns.length < 2) {
      setXField('')
      setYField('')
      return
    }
    setMode('row')
    setXField(result.columns[0])
    setYField(result.columns[1])
  }, [result])

  const displayResult = useMemo(() => {
    if (!result) return null
    if (result.columns.length <= 2) return result
    const measure = extractMeasure(result.mdx)
    if (mode === 'row') {
      const rows = result.rows.map(r => [r[0], r.slice(1).reduce((s, v) => s + toNumber(v), 0)])
      return { mdx: result.mdx, columns: [result.columns[0], measure], rows }
    } else {
      const rows = result.columns.slice(1).map((c, i) => [c, result.rows.reduce((s, r) => s + toNumber(r[i + 1]), 0)])
      return { mdx: result.mdx, columns: ['field', measure], rows }
    }
  }, [result, mode])

  const isMatrix = !!result && result.columns.length > 2

  useEffect(() => {
    if (!displayResult) return
    setXField(displayResult.columns[0])
    setYField(displayResult.columns[1])
  }, [displayResult])

  const options = displayResult?.columns || []
  const data = useMemo(() => {
    if (!displayResult) return []
    return displayResult.rows.map(r => {
      const obj: any = {}
      displayResult.columns.forEach((c, i) => (obj[c] = r[i]))
      return obj
    })
  }, [displayResult])

  return (
    <Box>
      <Typography variant="h6" sx={{ mb: 1 }}>График</Typography>
      <Stack direction="row" gap={2} sx={{ mb: 2 }}>
        {isMatrix && (
          <FormControl size="small" sx={{ minWidth: 200 }}>
            <InputLabel>Агрегация</InputLabel>
            <Select label="Агрегация" value={mode} onChange={e => setMode(e.target.value as any)}>
              <MenuItem value="row">По концернам</MenuItem>
              <MenuItem value="column">По месяцам</MenuItem>
            </Select>
          </FormControl>
        )}
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
