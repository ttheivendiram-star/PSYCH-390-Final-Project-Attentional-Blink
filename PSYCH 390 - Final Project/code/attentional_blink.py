import os, sys, pygame, random, string, csv

# -----------------------------
# Setup CSV file
# -----------------------------
script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
dataPath = os.path.join(script_directory, "SampleData.csv")

fieldnames = ["trial", "lag", "accuracy"]

# Only create the file and write headers if it doesn't exist yet
if not os.path.exists(dataPath):
    with open(dataPath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

# -----------------------------
# Setup Pygame
# -----------------------------
pygame.init()
mywindow = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("Arial", 36)
black = (0, 0, 0)

# -----------------------------
# Experiment parameters
# -----------------------------
n_trials = 6
cue_duration = 100  # ms — faster for stronger attentional blink effect
trial_count = 15

# -----------------------------
# Run trials
# -----------------------------
data_rows = []  # store all trial results for this participant

for trial_num_base in range(n_trials):
    trial_type = random.randint(1, 2)  # 1 = short lag, 2 = long lag
    target_num = random.randint(0, 9)
    target_num_alt = str(target_num)

    get_input = False
    response_made = False
    start = False
    start_response = False

    # Trial loop
    running_trial = True
    while running_trial:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not start and not start_response:
                if event.key == pygame.K_SPACE:
                    start = True
                    start_response = True
                else:
                    continue

            if event.type == pygame.KEYDOWN and get_input and not response_made:
                # Capture numeric response
                key_to_num = {
                    pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
                    pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7,
                    pygame.K_8: 8, pygame.K_9: 9
                }
                if event.key in key_to_num:
                    response_side = key_to_num[event.key]
                else:
                    continue

                # Check accuracy
                accuracy = 1 if response_side == target_num else 0
                response_made = True

                # Save trial data
                lag = 1 if trial_type == 1 else 5
                data_rows.append({"trial": trial_num_base + 1, "lag": lag, "accuracy": accuracy})

                # Print results
                print(f"Trial {trial_num_base + 1} | Lag={lag} | Response={response_side} | Correct={accuracy}")

                pygame.time.wait(1000)
                running_trial = False

        # -----------------------------
        # Draw screen
        # -----------------------------
        mywindow.fill((255, 255, 255))

        if not start and not get_input:
            text_surface = font.render('Press SPACE to start', False, black)
            mywindow.blit(text_surface, (200, 300))

        if start and not get_input:
            firstnum = str(random.randint(0, 9))
            stagger = 1 if trial_type == 1 else 5

            for seq_pos in range(trial_count):
                mywindow.fill((255, 255, 255))
                if seq_pos == 0:
                    text_surface = font.render(firstnum, False, black)
                elif seq_pos == stagger:
                    text_surface = font.render(target_num_alt, False, black)
                else:
                    random_letter = random.choice(string.ascii_letters)
                    text_surface = font.render(random_letter, False, black)
                mywindow.blit(text_surface, (400, 300))
                pygame.display.flip()
                pygame.time.wait(cue_duration)

            get_input = True

        if get_input and not response_made:
            text_surface = font.render('What was the second number?', False, black)
            mywindow.blit(text_surface, (100, 300))

        pygame.display.flip()
        clock.tick(60)

# -----------------------------
# Save participant data
# -----------------------------
with open(dataPath, "a", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerows(data_rows)

pygame.quit()
sys.exit()