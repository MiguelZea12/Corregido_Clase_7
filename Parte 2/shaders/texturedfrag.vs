#version 330 core

in vec3 color;
in vec3 normal;
in vec3 fragpos;
//in vec3 light_pos;
in vec3 view_pos;
out vec4 frag_color;

in vec2 UV;
uniform sampler2D tex;

struct light
{
  vec3 position;
  vec3 color;
};

#define NUM_LIGHTS 3
//uniform vec3 light_pos[NUM_LIGHTS];
uniform light light_data[NUM_LIGHTS];

vec4 Create_Light(vec3 light_pos, vec3 light_color, vec3 normal, vec3 fragpos, vec3 view_dir)
{
    //ambient light
    float a_strength = 0.1;
    vec3 ambient= a_strength * light_color;

    //diffuse light
    vec3 norm= normalize(normal);
    vec3 light_dir= normalize(light_pos- fragpos);
    float diff= max(dot(norm, light_dir), 0);
    vec3 diffuse= diff * light_color;

    //specular
    float s_strength=0.8;

    vec3 reflect_dir= normalize(-light_dir -norm);
    float spec= pow(max(dot(view_dir, reflect_dir), 0), 32);
    vec3 specular= s_strength * spec * light_color;

    return vec4(color * (ambient + diffuse + specular), 1.0f);

}


void main() {
    //vec3 light_color= vec3(1,0,0);

    vec3 view_dir= normalize(view_pos - fragpos);

    frag_color = Create_Light(light_data[0].position,light_data[0].color, normal, fragpos, view_dir);

    //for(int i = 0; i < NUM_LIGHTS; i++)
      //  frag_color += Create_Light(light_data[i].position, light_data[i].color, normal, fragpos, view_dir);

    frag_color = frag_color * texture(tex, UV);

}