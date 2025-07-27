export type Cube = { cube_name: string }
export type Measure = { measure_name: string; measure_unique_name: string; measure_group: string; format_string: string }
export type Dimension = { dimension_name: string; dimension_unique_name: string }
export type Hierarchy = { hierarchy_name: string; hierarchy_unique_name: string; dimension_unique_name: string }
export type Level = { level_name: string; level_unique_name: string; level_number: number }
export type Member = { caption: string; unique_name: string }
export type QueryRunResponse = { mdx: string; columns: string[]; rows: any[][] }
