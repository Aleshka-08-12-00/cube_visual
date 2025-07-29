import { useEffect, useMemo, useState } from 'react'
import { Box, Button, Grid2 as Grid, MenuItem, Select, Stack, TextField, Typography } from '@mui/material'
import { api } from '../api/client'
import { Cube, Measure, QueryRunResponse } from '../types'
import MeasureSelector from './MeasureSelector'
import DimensionTree from './DimensionTree'

type Props = { onResult: (r: QueryRunResponse) => void }

const EXAMPLE_QUERIES: Record<string, string> = {
  matrix: `WITH
SET [Months2024] AS
  NonEmpty(
    Descendants(
      [Время].[Год - Квартал - Месяц - День].&[2024],
      [Время].[Год - Квартал - Месяц - День].[Месяц]
    ),
    { [Measures].[реализация руб] }
  )
SELECT
  NON EMPTY
    [Months2024] * { [Measures].[реализация руб] }
  ON COLUMNS,
  NON EMPTY
    [Товар].[Концерн].Members
  ON ROWS
FROM [NextGen]`,
  concern: `SELECT
  NON EMPTY { [Measures].[реализация руб] } ON COLUMNS,
  NON EMPTY [Товар].[Концерн].Members ON ROWS
FROM [NextGen]`,
  month: `WITH
SET [Months2024] AS
  NonEmpty(
    Descendants(
      [Время].[Год - Квартал - Месяц - День].&[2024],
      [Время].[Год - Квартал - Месяц - День].[Месяц]
    ),
    { [Measures].[реализация руб] }
  )
SELECT
  NON EMPTY { [Measures].[реализация руб] } ON COLUMNS,
  NON EMPTY [Months2024] ON ROWS
FROM [NextGen]`,
}

const DEFAULT_MDX = EXAMPLE_QUERIES.matrix

export default function QueryBuilder({ onResult }: Props) {
  const [cubes, setCubes] = useState<Cube[]>([])
  const [cube, setCube] = useState('')
  const [measures, setMeasures] = useState<Measure[]>([])
  const [selMeasures, setSelMeasures] = useState<string[]>([])
  const [rowHierarchies, setRowHierarchies] = useState<string[]>([])
  const [colHierarchies, setColHierarchies] = useState<string[]>([])
  const [mdx, setMdx] = useState(DEFAULT_MDX)
  const [example, setExample] = useState('matrix')
  const canRun = useMemo(() => mdx.trim().length > 0 || (cube && selMeasures.length > 0), [mdx, cube, selMeasures])

  useEffect(() => {
    api.get<Cube[]>('/schema/cubes').then(r => {
      setCubes(r.data)
      if (r.data.length) setCube(r.data[0].cube_name)
    })
  }, [])

  useEffect(() => {
    setMdx(EXAMPLE_QUERIES[example])
  }, [example])

  useEffect(() => {
    // Run the default query once on mount so users immediately see results
    buildAndRun()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (!cube) return
    api.get<Measure[]>('/schema/measures', { params: { cube } }).then(r => setMeasures(r.data))
  }, [cube])

  const buildAndRun = async () => {
    const body = mdx.trim().length
      ? { mdx }
      : {
          cube,
          measures: selMeasures,
          rows: rowHierarchies.map(h => `${h}.Members`),
          columns: colHierarchies.map(h => `${h}.Members`),
          slicers: []
        }
    const r = await api.post<QueryRunResponse>('/query/run', body)
    onResult(r.data)
    setMdx(r.data.mdx)
  }

  return (
    <Stack gap={2}>
      <Typography variant="h6">Конструктор запроса</Typography>
      <Grid container spacing={2}>
        <Grid size={12}>
          <Stack direction="row" gap={2} alignItems="center" flexWrap="wrap">
            <Typography>Куб</Typography>
            <Select size="small" value={cube} onChange={e => setCube(e.target.value)} sx={{ minWidth: 200 }}>
              {cubes.map(c => (
                <MenuItem key={c.cube_name} value={c.cube_name}>{c.cube_name}</MenuItem>
              ))}
            </Select>
            <Typography>Пример</Typography>
            <Select size="small" value={example} onChange={e => setExample(e.target.value)} sx={{ minWidth: 280 }}>
              <MenuItem value="matrix">Концерн x Месяц (матрица)</MenuItem>
              <MenuItem value="concern">Реализация по концернам</MenuItem>
              <MenuItem value="month">Реализация по месяцам (2024)</MenuItem>
            </Select>
          </Stack>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <MeasureSelector measures={measures} selected={selMeasures} onChange={setSelMeasures} />
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <DimensionTree cube={cube} selectedHierarchies={rowHierarchies} onChange={setRowHierarchies} title="Строки" />
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <DimensionTree cube={cube} selectedHierarchies={colHierarchies} onChange={setColHierarchies} title="Колонки" />
        </Grid>
        <Grid size={12}>
          <TextField
            label="MDX"
            multiline
            minRows={6}
            fullWidth
            value={mdx}
            onChange={e => setMdx(e.target.value)}
            placeholder="Оставь пустым, чтобы использовать конструктор"
          />
        </Grid>
        <Grid size={12}>
          <Button variant="contained" disabled={!canRun} onClick={buildAndRun}>Выполнить</Button>
        </Grid>
      </Grid>
    </Stack>
  )
}
