import { Table, StringColumn } from '@servicenow/sdk/core'

export const x_d3doxp_test_probe = Table({
    name: 'x_d3doxp_test_probe',
    label: 'Test Probe',
    schema: {
        name: StringColumn({ label: 'Name', maxLength: 100 }),
        note: StringColumn({ label: 'Note', maxLength: 500 })
    }
})
