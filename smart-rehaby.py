import csv     # TableOfAllExercises.from_csv()
import random  # RehabPlan.random_plan()

from collections import OrderedDict
# other change
# mms

# Comments s s s s s s s s s


def main():
    # Load the Search Space.
    table = TableOfAllExercises.from_csv()

    # Ask the user for the target/goal Optimal Plan.
    optimal_plan = ask_for_optimal_plan()

    # Run the Genetic Algorithm.
    smart_rehab = SmartRehab(table, optimal_plan)

    smart_rehab.create_initial_population()

    # print(table)  # print search space
    # print()
    # print(smart_rehab)  # print population
    print()
    print('Fittest:  {}'.format(smart_rehab.fittest_fitness))
    print('The most suitable plan:  {}'.format(smart_rehab.fittest))
    print()

    # Output the results.
    rehab_plan = smart_rehab.fittest
    print('We are working on preparing your optimal rehabilitation plan...\n')
    rehab_plan.print_plan(smart_rehab.fittest_fitness)

    print('Hope you fast recovery!\n')


def ask_for_optimal_plan():
    name = input_loop('\nWelcome to SmartRehabilitation! What is your name?')

    age_category = input_loop(
        'Hi {}! Please enter your Age Category'
        ' (A for Adult and C for Child).'.format(name),
        {'A': Exercise.ADULT, 'C': Exercise.CHILD})

    condition_type = input_loop(
        'Please enter your Condition Type'
        ' (S for Stroke, SC for Spinal cord, and B for Brain injuries).',
        {'S': Exercise.STROKE, 'SC': Exercise.SPINAL_CORD_INJURY,
         'B': Exercise.BRAIN_INJURY})

    num_of_elbow = input_loop(
        'Please enter the number of exercises you prefer to perform for the'
        ' elbow (1 for one type, and 2 for two types of exercises).',
        {'1': 1, '2': 2})

    num_of_upper_arm = input_loop(
        'Please enter the number of exercises you prefer to perform for the'
        ' upper arm (1 for one type, and 2 for two types of exercises).',
        {'1': 1, '2': 2})

    num_of_knee_lower_leg = input_loop(
        'Please enter the number of exercises you prefer to perform for the'
        ' knee/lower leg (1 for one type, and 2 for two types of exercises).',
        {'1': 1, '2': 2})

    num_of_wrist = input_loop(
        'Please enter the number of exercises you prefer to perform for the'
        ' wrist (0 for no exercise, and 1 for one type of exercise).',
        {'0': 0, '1': 1})

    return OptimalPlan(
        age_category=age_category,
        condition_type=condition_type,

        num_of_elbow=num_of_elbow,
        num_of_upper_arm=num_of_upper_arm,
        num_of_knee_lower_leg=num_of_knee_lower_leg,
        num_of_wrist=num_of_wrist,
    )


def input_loop(text, options=None):
    while True:
        choice = input(text + '\n\n').strip()
        print()

        if options is None:
            if choice:
                return choice

            print('ERROR: Invalid input!')
        else:
            for option, value in options.items():
                if choice.lower() == option.lower():
                    return value

            print('ERROR: "{}" is an invalid choice!'.format(choice))


# The Genetic Algorithm and "Population"
class SmartRehab:
    def __init__(self, table, optimal_plan):
        self._table = table
        self._optimal_plan = optimal_plan

    def create_initial_population(self, population_size=70):
        self._population_size = population_size
        self._population = [
            RehabPlan.random_plan(self._table, self._optimal_plan)
            for i in range(population_size)
        ]  # list of population

        # to initialize array of zeros and it size = population size
        self._fitnesses = [0.0] * population_size

        self.compute_whole_individuals_fitness()

    def compute_whole_individuals_fitness(self):
        self._fittest = None
        self._fittest_fitness = 0.0

        # to loop through all the population and caculate the fitness to each one of them
        for i, rehab_plan in enumerate(self._population):
            fitness = rehab_plan.compute_fitness(self._optimal_plan)

            self._fitnesses[i] = fitness

            # to find the best fitness
            if self._fittest is None or fitness > self._fittest_fitness:
                self._fittest = rehab_plan
                self._fittest_fitness = fitness

    @property
    def population_size(self):
        return self._population_size

    @property
    def fittest(self):
        return self._fittest

    @property
    def fittest_fitness(self):
        return self._fittest_fitness

    def __repr__(self):
        buff = []

        for i, rehab_plan in enumerate(self._population):
            buff.append('{} => {}'.format(rehab_plan, self._fitnesses[i]))

        return '\n'.join(buff)


# One "Chromosome"/"Individual" in the "Population" (SmartRehab).
class RehabPlan:
    def __init__(self, table, exercises):
        self._table = table
        self._exercises = exercises

    @classmethod
    def random_plan(klass, table, optimal_plan):
        max_exercise_num = len(table)
        num_of_exercises = optimal_plan.num_of_exercises

        exercises = [random.randrange(max_exercise_num)
                     for i in range(num_of_exercises)]

        return klass(table, exercises)

    def compute_fitness(self, optimal_plan):
        # First, calculate the weighted sums.

        # to calculate the difference between the optimal and what the genetic generate
        age_category_sum = 0
        condition_type_sum = 0
        num_of_elbow = 0
        num_of_upper_arm = 0
        num_of_knee_lower_leg = 0
        num_of_wrist = 0

        # to get the exercises from the table after we collect the indexs randomly
        for i in self._exercises:
            exercise = self._table.get_exercise(i)

        # to check if the generated age and condition_type are the same as optimal (what the user entered)

            if exercise.age_category == optimal_plan.age_category:
                age_category_sum += 1
            if exercise.condition_type == optimal_plan.condition_type:
                condition_type_sum += 1

        # count the number of generated exercises
            if exercise.body_part == Exercise.ELBOW:
                num_of_elbow += 1
            elif exercise.body_part == Exercise.UPPER_ARM:
                num_of_upper_arm += 1
            elif exercise.body_part == Exercise.KNEE_LOWER_LEG:
                num_of_knee_lower_leg += 1
            elif exercise.body_part == Exercise.WRIST:
                num_of_wrist += 1

        # n => to calculate the difference between the optimal and generated
        # we use abs to avoid the impact of negative numbers
        # so that the increasing or decreasing of the number of exercises has the same affect
        # for example : if the optimal = 2 and the generated =1 has the same impact  if the optimal = 1 and the generated = 2

        n = 0
        n += abs(optimal_plan.num_of_elbow - num_of_elbow)
        n += abs(optimal_plan.num_of_upper_arm - num_of_upper_arm)
        n += abs(optimal_plan.num_of_knee_lower_leg - num_of_knee_lower_leg)
        n += abs(optimal_plan.num_of_wrist - num_of_wrist)

        # noe = number of exercises which mean the sum of the optimal exercises (what the user entered)
        # max_noe_sum = calculate all possible probabilities so that 4 = the number of the body parts in the table
        # num_of_exercises_sum = possible probabilities - difference between the optimal and generated
        noe = len(self._exercises)
        max_noe_sum = 4 * noe
        num_of_exercises_sum = max_noe_sum - n

        # as mentioed in the questions Age Category and number of Exercises should be equally important,
        # but half as important as the Condition Type.

        fitness = 0.0
        fitness += 0.25 * (age_category_sum / noe)
        fitness += 0.25 * (num_of_exercises_sum / max_noe_sum)
        fitness += 0.50 * (condition_type_sum / noe)

        return fitness

    def print_plan(self, fitness=None):
        print(
            'Your rehabilitation plan is ready! Your plan is presented below'
            ' with {} exercises per day.\n'.format(self.len_as_word())
        )

        # if fitness:
        #     print('Fitness: {}, {}, [ {} ]\n'.format(
        #         fitness, str(self),
        #         ', '.join([str(e) for e in self._exercises])))

        # OrderedDict to output in correct order of Body Part.
        plan = OrderedDict([
            [Exercise.ELBOW, []],
            [Exercise.UPPER_ARM, []],
            [Exercise.KNEE_LOWER_LEG, []],
            [Exercise.WRIST, []],
        ])

        # to show all the exercises in one row
        for i in self._exercises:
            exercise = self._table.get_exercise(i)

            by_body_part = plan[exercise.body_part]
            by_body_part.append(exercise)

        for body_part, exercises in plan.items():
            buff = '{}:'.format(body_part)

            for i, exercise in enumerate(exercises):
                buff += ' {}. {}.'.format(i + 1, exercise.exercise)

            print(buff + '\n')

    def len_as_word(self):
        words = [
            'zero', 'one', 'two', 'three', 'four', 'five',
            'six', 'seven', 'eight', 'nine', 'ten',
        ]

        length = len(self._exercises)

        if length < len(words):
            return words[length]
        else:
            return str(length)

    def __len__(self):
        return len(self._exercises)

    def __repr__(self):
        buff = '[ '

        for i in self._exercises:
            exercise = self._table.get_exercise(i)

            buff += '{}{}{} '.format(
                exercise.body_part[0],
                exercise.condition_type[1],
                exercise.age_category[0],
            )

        return buff + ']'


class OptimalPlan:
    def __init__(self, age_category, condition_type, num_of_elbow,
                 num_of_upper_arm, num_of_knee_lower_leg, num_of_wrist):
        if age_category not in Exercise.AGE_CATEGORIES:
            raise ValueError('Invalid age category: ' + age_category)
        if condition_type not in Exercise.CONDITION_TYPES:
            raise ValueError('Invalid condition type: ' + condition_type)

        if num_of_elbow not in [1, 2]:
            raise ValueError('Number of elbow exercises must be 1 or 2: '
                             + num_of_elbow)
        if num_of_upper_arm not in [1, 2]:
            raise ValueError('Number of upper arm exercises must be 1 or 2: '
                             + num_of_upper_arm)
        if num_of_knee_lower_leg not in [1, 2]:
            raise ValueError(
                'Number of knee/lower leg exercises must be 1 or 2: '
                + num_of_knee_lower_leg)
        if num_of_wrist not in [0, 1]:
            raise ValueError('Number of wrist exercises must be 0 or 1: '
                             + num_of_wrist)

        self._age_category = age_category
        self._condition_type = condition_type

        self._num_of_elbow = num_of_elbow
        self._num_of_upper_arm = num_of_upper_arm
        self._num_of_knee_lower_leg = num_of_knee_lower_leg
        self._num_of_wrist = num_of_wrist

        self._num_of_exercises = (
            num_of_elbow
            + num_of_upper_arm
            + num_of_knee_lower_leg
            + num_of_wrist
        )

    @property
    def age_category(self):
        return self._age_category

    @property
    def condition_type(self):
        return self._condition_type

    @property
    def num_of_elbow(self):
        return self._num_of_elbow

    @property
    def num_of_upper_arm(self):
        return self._num_of_upper_arm

    @property
    def num_of_knee_lower_leg(self):
        return self._num_of_knee_lower_leg

    @property
    def num_of_wrist(self):
        return self._num_of_wrist

    @property
    def num_of_exercises(self):
        return self._num_of_exercises


# The "Search Space" (table of exercise data from CSV file).
class TableOfAllExercises:
    def __init__(self):
        self._data = []

    @classmethod
    def from_csv(klass, filename='smart_rehab.csv'):  # read from csv
        table = klass()
        table.add_from_csv(filename)

        return table

    def add_from_csv(self, filename):
        with open(filename, 'rt') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    self.add_exercise(Exercise(
                        row['Body Part'],
                        row['Exercise'],
                        row['Condition Type'],
                        row['Age Category'],
                    ))
                except ValueError as e:
                    raise ValueError(
                        'Invalid value from CSV row: ' + str(row)) from e

    def add_exercise(self, exercise):
        self._data.append(exercise)

    def get_exercise(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        buff = []

        for i, exercise in enumerate(self._data):
            buff.append('{} => {}'.format(i, exercise))

        return '\n'.join(buff)


# The data from a CSV row.
class Exercise:
    # Body Parts.
    ELBOW = 'Elbow'
    UPPER_ARM = 'Upper Arm'
    KNEE_LOWER_LEG = 'Knee/Lower leg'
    WRIST = 'Wrist'
    BODY_PARTS = {ELBOW, UPPER_ARM, KNEE_LOWER_LEG, WRIST}

    # Condition Types.
    STROKE = 'Stroke'
    SPINAL_CORD_INJURY = 'Spinal cord injuries'
    BRAIN_INJURY = 'Brain injury'
    CONDITION_TYPES = {STROKE, SPINAL_CORD_INJURY, BRAIN_INJURY}

    # Age Categories.
    ADULT = 'Adult'
    CHILD = 'Child'
    AGE_CATEGORIES = {ADULT, CHILD}

    def __init__(self, body_part, exercise, condition_type, age_category):
        if body_part not in self.BODY_PARTS:
            raise ValueError('Invalid body part: ' + body_part)
        if condition_type not in self.CONDITION_TYPES:
            raise ValueError('Invalid condition type: ' + condition_type)
        if age_category not in self.AGE_CATEGORIES:
            raise ValueError('Invalid age category: ' + age_category)

        self._body_part = body_part
        self._exercise = exercise
        self._condition_type = condition_type
        self._age_category = age_category

    @property
    def body_part(self):
        return self._body_part

    @property
    def exercise(self):
        return self._exercise

    @property
    def condition_type(self):
        return self._condition_type

    @property
    def age_category(self):
        return self._age_category

    def __repr__(self):
        return '[ {}, {}, {}, {} ]'.format(
            self._body_part,
            self._condition_type,
            self._age_category,
            self._exercise,
        )


if __name__ == '__main__':
    main()
