<template>
    <b-card>
        <h2 class="contest-title">{{ eventData.event_name }}</h2>
        <p class="contest-description">{{ eventData.event_description }}</p>
        <p class="contest-description">
            Статус мероприятия: {{ eventLevelName }}
        </p>
        <p class="contest-evaluation-method">
            Метод оценивания: {{ displayEvaluationMethod }}
        </p>
        <div v-if="user.role === 'organizer'">
            <div style="display: flex; justify-content: space-between;">
                <nuxt-link
                    :to="'/settings?id=' + eventData.id"
                    class="contest-manage_edit_button"
                    >Редактировать</nuxt-link
                >
                <nuxt-link
                    :to="`/nominations?eventid=${eventData.id}&`"
                    class="contest-manage_edit_button ml-3"
                    >Управление номинациями</nuxt-link
                >
                <a
                    class="contest-manage_delete_button"
                    @click="$emit('deleteEvent', eventData)"
                    >Удалить</a
                >
            </div>
        </div>
        <div v-else>
            <div style="display: flex; justify-content: start;">
                <nuxt-link
                    :to="`/nominations?eventid=${eventData.id}&`"
                    class="contest-manage_edit_button"
                    >Просмотр номинаций</nuxt-link
                >

            </div>
        </div>  
    </b-card>
</template>

<script>
import { mapGetters } from "vuex";
export default {
    props: {
        eventData: {
            type: Object,
            required: true
        }
    },
    computed: {
        eventLevelName() {
            const levels = ['Университетское', 'Региональное', 'Межрегиональное', 'Всероссийское', 'Международное'];
            const level = this.eventData.event_level;
            // Ensure level is within the expected range
            if (level >= 0 && level < levels.length) {
                return levels[level];
            }
            return 'Неизвестный статус'; // Fallback for out of range values
        },
        displayEvaluationMethod() {
        const methods = {
            0: 'Арифметический',
            1: 'Рейтинговый'
        };
        return methods[this.eventData.evaluation_method] || "Нет данных";
        },
        ...mapGetters({
            user: "getUser",
        }),
    }
}
</script>

<style scoped>
.contest-title {
  margin-bottom: 10px;
  font-size: 24px;
  font-weight: 700;
  color: #464646;
}
.contest-description,
.contest-experts,
.contest-period {
  font-size: 15px;
  font-weight: 300;
  color: #474747;
}
.contest-evaluation-method {
  color: #616161;
}
.contest-manage_edit_button {
  /* color: #616161; */
  cursor: pointer;
  text-decoration: none;
  /* margin-left: 10px; */
}
.contest-manage_delete_button {
  color: #be6363;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.1s ease;
  margin-left: auto;
  margin-right: 15px;
}

</style>