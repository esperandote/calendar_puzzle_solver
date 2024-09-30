<template>
  <div>
    <div class="puzzle">
      <div
        v-for="(line, line_index) in state"
        class="line"
        >
        <div
          v-for="(square, square_index) in line"
          :class="{
            'square': true,
            'unvisible': square === 1,
            'filled': square === 2,
            'color1': square === 3,
            'color2': square === 4,
            'color3': square === 5,
            'color4': square === 6,
            'color5': square === 7,
            'color6': square === 8,
            'color7': square === 9,
            'color8': square === 10,
            'color9': square === 11,
            'color10': square === 12,
          }"
          @click="select(line_index, square_index)"
          >
          {{ texts[line_index * 7 + square_index] }}
        </div>
      </div>
    </div>
    <div class="btns">
      <a-button @click="solve" :disabled="selected_count !== 3" :loading="loading">
        Solve
      </a-button>
      <a-button @click="fetchInitData">
        Refresh
      </a-button>
    </div>
  </div>
</template>

<script>
import { message } from 'ant-design-vue';
import { getRequest, postRequest } from './utils/requests'
export default {
  name: "Solver",
  data: function () {
    return {
      // filled_indices: [],
      // rotation_indices: [],
      // positions: [],
      selected_count: 0,
      elements: [],
      state: [],
      loading: false,
      texts: [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "",
        "1", "2", "3", "4", "5", "6", "7",
        "8", "9", "10", "11", "12", "13", "14",
        "15", "16", "17", "18", "19", "20", "21",
        "22", "23", "24", "25", "26", "27", "18",
        "29", "30", "31", "Sun", "Mon", "Tue", "Wed",
        "", "", "", "", "Thur", "Fri", "Sat" 
      ]
      // 0 for empty
      // 1 for unvisible
      // 2 for filled
      // 3~12 for different colors
    }
  },
  async mounted() {
    await this.fetchInitData()
  },
  methods: {
    async fetchInitData () {
      const init_data = await getRequest("/init_data", {})
      this.elements = init_data.elements
      this.state = init_data.origin_state
      this.selected_count = 0
    },
    async solve() {
      const filled_indices = []
      for (let line_index = 0; line_index < this.state.length; line_index += 1) {
        for (let square_index = 0; square_index < 7; square_index += 1) {
          if (this.state[line_index][square_index] === 2) {
            filled_indices.push(line_index * 7 + square_index)
          }
        }
      }
      const start_time = Date.now()
      this.loading = true
      const response = await postRequest(
        "/solve",
        { filled_indices: filled_indices }
      )
      this.loading = false
      message.info("Time Consumption: " + (Date.now() - start_time)/1000 + " s")
      console.log(Date.now() - start_time)
      const rotation_indices = response.rotation_indices
      const positions = response.positions
      if(rotation_indices.length !== 10 || positions.length !== 10) {
        return
      }
      for (let index = 0; index < 10; index++) {
        const rotation = this.elements[index][rotation_indices[index]]
        const position = positions[index]
        for (let k of rotation) {
          const j = position % 7
          const i = (position - j) / 7
          const j_offset = k % 7
          const i_offset = (k - j_offset) / 7
          this.state[i + i_offset][j + j_offset] = index + 3
        }
      }
    },
    select(line_index, square_index) {
      if(this.state[line_index][square_index] === 0) {
        if (this.selected_count === 3) {
          return
        }
        this.state[line_index][square_index] = 2
        this.selected_count += 1
        return
      }
      if(this.state[line_index][square_index] === 2) {
        this.state[line_index][square_index] = 0
        this.selected_count -= 1
        return
      }
    }
  }
}
</script>

<style scoped>
div.line {
  margin-bottom: 5px;
  height: 50px;
}
div.line > div.square {
  float: left;
  width: 50px;
  height: 50px;
  margin-right: 5px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-family: monospace;
  color: #777;
}
.square {
  background-color: #ddd;
}
.unvisible {
  background-color: #fff;
}
.filled {
  background-color: #bbb;
}
.color1 {
  background-color: #fcc;
}
.color2 {
  background-color: #ff9;
}
.color3 {
  background-color: #cfc;
}
.color4 {
  background-color: #9ff;
}
.color5 {
  background-color: #bdf;
}
.color6 {
  background-color: #dbf;
}
.color7 {
  background-color: #fcf;
}
.color8 {
  background-color: #fdb;
}
.color9 {
  background-color: #dfb;
}
.color10 {
  background-color: #fea;
}
</style>
